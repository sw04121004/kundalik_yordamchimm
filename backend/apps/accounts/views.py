from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


from .serializers import (
    ChangePasswordSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

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


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return UpdateProfileSerializer
        return UserSerializer


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Parol muvaffaqiyatli o‘zgartirildi."})
