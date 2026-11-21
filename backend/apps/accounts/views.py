from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import logging
import requests
import secrets
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from .throttles import LoginThrottle, PasswordChangeThrottle, RegisterThrottle, PasswordResetThrottle, PasswordResetConfirmThrottle
from .models import PasswordResetCode
UserModel = get_user_model()
logger = logging.getLogger(__name__)


from .serializers import (
    ChangePasswordSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    DeleteAccountSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottle]

    def create(self, request, *args, **kwargs):
        lang = _get_lang_from_request(request)
        from django.utils import translation
        translation.activate(lang)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=201,
            )
        finally:
            translation.deactivate()


class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    """Allow logging in with either username or email.

    The serializer now accepts an optional ``email`` field. If ``email`` is provided
    it is used to look up the user and the corresponding ``username`` is injected
    into the data before the parent validation runs.
    """
    email = serializers.EmailField(write_only=True, required=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        # Resolve username/email case-insensitively and discard accidental spaces.
        login_value = (attrs.get(self.username_field) or attrs.get("email") or "").strip()
        password = attrs.get("password")
        if login_value:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            # 1. Agar username aniq mos kelsa faqat shu user:
            user_by_username = User.objects.filter(username__iexact=login_value).first()
            if user_by_username:
                attrs[self.username_field] = user_by_username.username
            elif "@" in login_value:
                # 2. Email bilan kirilganda barcha faol userlarni tekshirish:
                candidates = User.objects.filter(email__iexact=login_value, is_active=True).order_by("-last_login", "-date_joined", "-id")
                matched_user = None
                if password:
                    for cand in candidates:
                        if cand.check_password(password):
                            matched_user = cand
                            break
                if matched_user:
                    attrs[self.username_field] = matched_user.username
                elif candidates.exists():
                    attrs[self.username_field] = candidates.first().username
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailOrUsernameTokenSerializer
    throttle_classes = [LoginThrottle]


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return UpdateProfileSerializer
        return UserSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        raw_refresh = request.data.get("refresh")
        if not isinstance(raw_refresh, str) or not raw_refresh:
            return Response({"detail": "Refresh token yuborilmadi."}, status=400)

        try:
            refresh = RefreshToken(raw_refresh)
        except TokenError:
            return Response({"detail": "Refresh token yaroqsiz yoki muddati tugagan."}, status=400)

        if str(refresh.get("user_id")) != str(request.user.pk):
            return Response({"detail": "Bu refresh token joriy akkauntga tegishli emas."}, status=403)

        try:
            refresh.blacklist()
        except AttributeError:
            return Response({"detail": "Token blacklist xizmati sozlanmagan."}, status=503)
        except TokenError:
            return Response({"detail": "Refresh token allaqachon bekor qilingan."}, status=400)
        return Response({"detail": "Sessiya yakunlandi."})


class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            for outstanding in OutstandingToken.objects.filter(user=request.user):
                BlacklistedToken.objects.get_or_create(token=outstanding)
            request.user.delete()

        return Response(status=204)


_EMAIL_NOT_CONFIGURED = {
    "uz": "Email yuborish sozlanmagan. Administrator pochta xizmatini sozlashi kerak.",
    "ru": "Отправка email не настроена. Администратору необходимо настроить почтовый сервис.",
    "en": "Email sending is not configured. The administrator needs to configure the email service.",
}

_EMAIL_SENT_DETAIL = {
    "uz": "Agar email akkauntga tegishli bo'lsa, tiklash kodi yuborildi.",
    "ru": "Если email принадлежит аккаунту, код для восстановления был отправлен.",
    "en": "If the email is associated with an account, a reset code has been sent.",
}

_RESET_EMAIL_TEMPLATES = {
    "uz": {
        "subject": "Qulay.uz — parolni tiklash kodi",
        "text": "Parolni tiklash kodi: {code}. Kod 10 daqiqa amal qiladi.",
        "html": "<p>Parolni tiklash kodi: <strong>{code}</strong>.</p><p>Kod 10 daqiqa amal qiladi.</p>",
    },
    "ru": {
        "subject": "Qulay.uz — код восстановления пароля",
        "text": "Код восстановления пароля: {code}. Код действителен 10 минут.",
        "html": "<p>Код восстановления пароля: <strong>{code}</strong>.</p><p>Код действителен 10 минут.</p>",
    },
    "en": {
        "subject": "Qulay.uz — password reset code",
        "text": "Password reset code: {code}. The code is valid for 10 minutes.",
        "html": "<p>Password reset code: <strong>{code}</strong>.</p><p>The code is valid for 10 minutes.</p>",
    },
}


def _get_lang_from_request(request):
    if not request:
        return "uz"
    accept = ""
    if hasattr(request, "headers") and request.headers:
        accept = request.headers.get("Accept-Language") or ""
    if not accept and hasattr(request, "META"):
        accept = request.META.get("HTTP_ACCEPT_LANGUAGE") or ""
    if not accept:
        from django.utils import translation
        active = translation.get_language()
        if active in ("uz", "ru", "en"):
            return active
        return "uz"
    for part in accept.split(","):
        tag = part.split(";")[0].strip().lower()
        base_tag = tag.split("-")[0]
        if base_tag in ("uz", "ru", "en"):
            return base_tag
    return "uz"


def is_email_configured():
    provider = getattr(settings, "EMAIL_PROVIDER", "brevo").lower().strip()
    if provider == "brevo":
        return bool(getattr(settings, "BREVO_API_KEY", "").strip())
    if provider == "smtp":
        if getattr(settings, "EMAIL_BACKEND", "").endswith("smtp.EmailBackend"):
            return bool(getattr(settings, "EMAIL_HOST", "").strip() and (getattr(settings, "DEFAULT_FROM_EMAIL", "").strip() or getattr(settings, "EMAIL_FROM", "").strip()))
        return True
    if provider in ("console", "locmem") or getattr(settings, "EMAIL_BACKEND", "").endswith(("console.EmailBackend", "locmem.EmailBackend")):
        return True
    return bool(getattr(settings, "BREVO_API_KEY", "").strip() or getattr(settings, "EMAIL_HOST", "").strip())


def send_brevo_email(to_email, subject, text_content, html_content=None):
    sender_email = getattr(settings, "EMAIL_FROM", "") or getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@qulay.uz") or "noreply@qulay.uz"
    sender_name = getattr(settings, "EMAIL_FROM_NAME", "Qulay.uz") or "Qulay.uz"
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": text_content,
    }
    if html_content:
        payload["htmlContent"] = html_content
    res = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": getattr(settings, "BREVO_API_KEY", ""),
            "content-type": "application/json",
        },
        json=payload,
        timeout=getattr(settings, "EMAIL_TIMEOUT", 10),
    )
    if res.status_code not in (200, 201, 202):
        logger.error(f"Brevo API error: status={res.status_code}, response={res.text}")
        raise RuntimeError(f"Brevo API failed with status {res.status_code}")
    return True


def send_password_reset_email(to_email, code, lang="uz"):
    template = _RESET_EMAIL_TEMPLATES.get(lang, _RESET_EMAIL_TEMPLATES["uz"])
    subject = template["subject"]
    text_content = template["text"].format(code=code)
    html_content = template["html"].format(code=code)
    provider = getattr(settings, "EMAIL_PROVIDER", "brevo").lower().strip()

    if provider == "brevo":
        return send_brevo_email(to_email, subject, text_content, html_content)
    else:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or getattr(settings, "EMAIL_FROM", "noreply@qulay.uz")
        send_mail(
            subject,
            text_content,
            from_email,
            [to_email],
            fail_silently=False,
        )
        return True


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PasswordResetThrottle]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lang = _get_lang_from_request(request)

        if not is_email_configured():
            return Response({"detail": _EMAIL_NOT_CONFIGURED[lang]}, status=503)

        email_clean = serializer.validated_data["email"].strip()
        candidates = UserModel.objects.filter(email__iexact=email_clean, is_active=True).order_by("-last_login", "-date_joined", "-id")
        account = candidates.first()
        if not account:
            account = UserModel.objects.filter(email__iexact=email_clean).order_by("-date_joined", "-id").first()
        generic_detail = _EMAIL_SENT_DETAIL[lang]

        if account:
            now = timezone.now()
            PasswordResetCode.objects.filter(user__email__iexact=email_clean, used_at__isnull=True).update(used_at=now)
            code = f"{secrets.randbelow(1_000_000):06d}"
            reset = PasswordResetCode.objects.create(
                user=account,
                code_hash=make_password(code),
                expires_at=now + timedelta(minutes=10),
            )
            try:
                send_password_reset_email(account.email, code, lang=lang)
            except Exception:
                logger.error("Password reset email delivery failed.", exc_info=True)
                reset.used_at = timezone.now()
                reset.save(update_fields=["used_at"])
                # If email sending fails, treat it as a successful request to avoid leaking configuration details.
                # Mark the reset code as used to prevent reuse, then return the standard success response.
                return Response({"detail": _EMAIL_SENT_DETAIL[lang]}, status=202)

        return Response({"detail": generic_detail}, status=202)


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PasswordResetConfirmThrottle]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip()
        code = serializer.validated_data["code"].strip()
        new_password = serializer.validated_data["new_password"]
        now = timezone.now()
        lang = _get_lang_from_request(request)

        with transaction.atomic():
            reset = PasswordResetCode.objects.select_for_update().select_related("user").filter(
                user__email__iexact=email,
                used_at__isnull=True,
                expires_at__gt=now,
                attempts__lt=5,
            ).order_by("-created_at").first()

            if not reset:
                msg = {
                    "uz": "Kod yaroqsiz yoki muddati tugagan. Yangi kod so'rang.",
                    "ru": "Код недействителен или срок его действия истёк. Запросите новый код.",
                    "en": "The code is invalid or expired. Request a new code.",
                }.get(lang, "Kod yaroqsiz yoki muddati tugagan. Yangi kod so'rang.")
                return Response({"detail": msg}, status=400)

            if not check_password(code, reset.code_hash):
                reset.attempts += 1
                reset.save(update_fields=["attempts"])
                msg = {
                    "uz": "Tasdiqlash kodi noto'g'ri.",
                    "ru": "Неверный код подтверждения.",
                    "en": "Incorrect confirmation code.",
                }.get(lang, "Tasdiqlash kodi noto'g'ri.")
                return Response({"detail": msg}, status=400)

            target_user = reset.user
            target_user.set_password(new_password)
            target_user.save()

            reset.used_at = now
            reset.save(update_fields=["used_at"])

            for outstanding in OutstandingToken.objects.filter(user=target_user):
                BlacklistedToken.objects.get_or_create(token=outstanding)

        success_msg = {
            "uz": "Parol o'zgartirildi. Yangi parol bilan tizimga kiring.",
            "ru": "Пароль изменён. Войдите в систему с новым паролем.",
            "en": "Password changed. Log in with your new password.",
        }.get(lang, "Parol o'zgartirildi. Yangi parol bilan tizimga kiring.")
        return Response({"detail": success_msg})


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [PasswordChangeThrottle]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        for outstanding in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=outstanding)

        lang = _get_lang_from_request(request)
        msg = {
            "uz": "Parol muvaffaqiyatli o‘zgartirildi.",
            "ru": "Пароль успешно изменён.",
            "en": "Password changed successfully.",
        }.get(lang, "Parol muvaffaqiyatli o‘zgartirildi.")
        return Response({"detail": msg})
