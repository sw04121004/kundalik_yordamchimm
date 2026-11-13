from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()

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


def _validate_password_for_request(password, user, request):
    language = (request.headers.get("Accept-Language", "uz").split(",", 1)[0].split("-", 1)[0].lower())
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
        }

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Bu foydalanuvchi nomi allaqachon band.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan.")
        return value

    def validate_password(self, value):
        request = self.context["request"]
        validation_user = User(
            username=self.initial_data.get("username", ""),
            email=self.initial_data.get("email", ""),
            first_name=self.initial_data.get("first_name", ""),
        )
        _validate_password_for_request(value, validation_user, request)
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Parollar mos kelmadi."})
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
        if value:
            qs = User.objects.filter(email__iexact=value).exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        request = self.context["request"]
        _validate_password_for_request(value, request.user, request)
        return value

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Joriy parol noto‘g‘ri.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Yangi parollar mos kelmadi."})
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
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Yangi parollar mos kelmadi."})
        user = User.objects.filter(email__iexact=attrs["email"]).first()
        _validate_password_for_request(attrs["new_password"], user, self.context["request"])
        return attrs


class DeleteAccountSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Joriy parol noto‘g‘ri.")
        return value
