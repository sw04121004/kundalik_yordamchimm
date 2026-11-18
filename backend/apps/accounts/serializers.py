from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


def _get_language_from_request(request):
    if not request:
        return "uz"
    accept = getattr(request, "headers", {}).get("Accept-Language", "uz") if hasattr(request, "headers") else request.META.get("HTTP_ACCEPT_LANGUAGE", "uz")
    lang = accept.split(",", 1)[0].split("-", 1)[0].lower()
    return lang if lang in ("uz", "ru", "en") else "uz"


_PASSWORD_MESSAGES = {
    "uz": {
        "password_too_short": "Parol kamida 8 belgidan iborat bo‘lishi kerak.",
        "password_too_common": "Bu parol juda keng tarqalgan. Boshqa, murakkabroq parol tanlang.",
        "password_entirely_numeric": "Parol faqat raqamlardan iborat bo‘lmasin.",
        "password_too_similar": "Parol foydalanuvchi ma’lumotlariga juda o‘xshash bo‘lmasin.",
    },
    "ru": {
        "password_too_short": "Пароль должен содержать не менее 8 символов.",
        "password_too_common": "Этот пароль слишком распространён. Выберите более сложный пароль.",
        "password_entirely_numeric": "Пароль не должен состоять только из цифр.",
        "password_too_similar": "Пароль не должен быть слишком похож на данные пользователя.",
    },
    "en": {
        "password_too_short": "The password must contain at least 8 characters.",
        "password_too_common": "This password is too common. Choose a less predictable password.",
        "password_entirely_numeric": "The password cannot consist only of numbers.",
        "password_too_similar": "The password is too similar to the user's information.",
    },
}

_REGISTER_MESSAGES = {
    "uz": {
        "username_taken": "Bu foydalanuvchi nomi allaqachon band.",
        "email_taken": "Bu email allaqachon ro‘yxatdan o‘tgan.",
        "password_mismatch": "Parollar mos kelmadi.",
    },
    "ru": {
        "username_taken": "Пользователь с таким именем уже существует.",
        "email_taken": "Этот адрес электронной почты уже зарегистрирован.",
        "password_mismatch": "Пароли не совпадают.",
    },
    "en": {
        "username_taken": "A user with that username already exists.",
        "email_taken": "This email is already registered.",
        "password_mismatch": "Passwords do not match.",
    },
}

_AUTH_ACTION_MESSAGES = {
    "uz": {
        "current_password_wrong": "Joriy parol noto‘g‘ri.",
        "new_passwords_mismatch": "Yangi parollar mos kelmadi.",
        "confirmation_invalid": "Tasdiqlash uchun «O'chirish» deb yozing.",
    },
    "ru": {
        "current_password_wrong": "Неверный текущий пароль.",
        "new_passwords_mismatch": "Новые пароли не совпадают.",
        "confirmation_invalid": "Для подтверждения введите «Удалить».",
    },
    "en": {
        "current_password_wrong": "Incorrect current password.",
        "new_passwords_mismatch": "New passwords do not match.",
        "confirmation_invalid": "Type \"Delete\" to confirm.",
    },
}

ALLOWED_CONFIRMATION_WORDS = {"o'chirish", "ochirish", "удалить", "delete"}


def normalize_confirmation_word(text: str) -> str:
    if not text:
        return ""
    import re
    normalized = re.sub(r"[\’\ʻ\ʼ\‘\`\´\′]", "'", str(text).strip().lower())
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def _validate_password_for_request(password, user, request):
    language = _get_language_from_request(request)
    messages = _PASSWORD_MESSAGES.get(language, _PASSWORD_MESSAGES["uz"])
    try:
        validate_password(password, user=user)
    except DjangoValidationError as exc:
        codes = {error.code for error in exc.error_list}
        ordered = ("password_too_short", "password_too_common", "password_entirely_numeric", "password_too_similar")
        raise serializers.ValidationError([messages[code] for code in ordered if code in codes] or [
            "Parol xavfsizlik talablariga mos kelmadi." if language == "uz" else
            "Пароль не соответствует требованиям безопасности." if language == "ru" else
            "The password does not meet security requirements."
        ]) from None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "date_joined")
        read_only_fields = ("id", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "password", "password2")
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "first_name": {"required": False, "allow_blank": True},
            "username": {
                "validators": [],  # Avoid DRF's default English UniqueValidator
            },
        }

    def validate_username(self, value):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        clean_value = (value or "").strip()
        if User.objects.filter(username__iexact=clean_value).exists():
            raise serializers.ValidationError(_REGISTER_MESSAGES[lang]["username_taken"])
        return clean_value

    def validate_email(self, value):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        if value:
            clean_value = value.strip()
            if User.objects.filter(email__iexact=clean_value).exists():
                raise serializers.ValidationError(_REGISTER_MESSAGES[lang]["email_taken"])
            return clean_value
        return value

    def validate_password(self, value):
        request = self.context.get("request")
        validation_user = User(
            username=self.initial_data.get("username", ""),
            email=self.initial_data.get("email", ""),
            first_name=self.initial_data.get("first_name", ""),
        )
        _validate_password_for_request(value, validation_user, request)
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": _REGISTER_MESSAGES[lang]["password_mismatch"]})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "email")

    def validate_email(self, value):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        if value:
            clean_value = value.strip()
            qs = User.objects.filter(email__iexact=clean_value).exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(_REGISTER_MESSAGES[lang]["email_taken"])
            return clean_value
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        request = self.context.get("request")
        _validate_password_for_request(value, request.user, request)
        return value

    def validate_old_password(self, value):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError(_AUTH_ACTION_MESSAGES[lang]["current_password_wrong"])
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": _AUTH_ACTION_MESSAGES[lang]["new_passwords_mismatch"]})
        _validate_password_for_request(attrs["new_password"], self.context["request"].user, self.context["request"])
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(r"^\d{6}$")
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": _AUTH_ACTION_MESSAGES[lang]["new_passwords_mismatch"]})
        user = User.objects.filter(email__iexact=attrs["email"]).first()
        _validate_password_for_request(attrs["new_password"], user, self.context["request"])
        return attrs


class DeleteAccountSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirmation = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_current_password(self, value):
        request = self.context.get("request")
        lang = _get_language_from_request(request)
        if not request.user.check_password(value):
            raise serializers.ValidationError(_AUTH_ACTION_MESSAGES[lang]["current_password_wrong"])
        return value

    def validate(self, attrs):
        conf = attrs.get("confirmation")
        if conf is not None and conf != "":
            normalized = normalize_confirmation_word(conf)
            if normalized not in ALLOWED_CONFIRMATION_WORDS:
                request = self.context.get("request")
                lang = _get_language_from_request(request)
                raise serializers.ValidationError({"confirmation": _AUTH_ACTION_MESSAGES[lang]["confirmation_invalid"]})
        return attrs
