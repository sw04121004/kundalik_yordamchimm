from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    scope = "auth_login"


class RegisterThrottle(UserRateThrottle):
    scope = "auth_register"


class PasswordChangeThrottle(UserRateThrottle):
    scope = "auth_password_change"


from rest_framework.throttling import AnonRateThrottle


class PasswordResetThrottle(AnonRateThrottle):
    scope = "auth_password_reset"


class PasswordResetConfirmThrottle(AnonRateThrottle):
    scope = "auth_password_reset_confirm"
