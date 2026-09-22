from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)
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
        # Prefer explicit ``username`` if supplied, otherwise fall back to ``email``
        login_value = attrs.get(self.username_field) or attrs.get("email")
        if login_value:
            # If the value contains an '@' we treat it as an email address
            if "@" in login_value:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    matched = User.objects.get(email__iexact=login_value)
                    attrs[self.username_field] = matched.username
                except User.DoesNotExist:
                    # Let the parent validation raise an appropriate error
                    pass
            else:
                attrs[self.username_field] = login_value
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailOrUsernameTokenSerializer

    def post(self, request, *args, **kwargs):
        logger.info("🔎 Login payload received: %s", request.data)
        return super().post(request, *args, **kwargs)


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
