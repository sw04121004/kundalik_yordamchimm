from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db import transaction
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from .throttles import LoginThrottle, PasswordChangeThrottle, RegisterThrottle


from .serializers import (
    ChangePasswordSerializer,
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
        if login_value:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            lookup = {"email__iexact": login_value} if "@" in login_value else {"username__iexact": login_value}
            matched = User.objects.filter(**lookup).first()
            if matched:
                attrs[self.username_field] = matched.username
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


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [PasswordChangeThrottle]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Parol muvaffaqiyatli o‘zgartirildi."})
