from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    scope = "auth_login"


class RegisterThrottle(UserRateThrottle):
    scope = "auth_register"


class PasswordChangeThrottle(UserRateThrottle):
    scope = "auth_password_change"
