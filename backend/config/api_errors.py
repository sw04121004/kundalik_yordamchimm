from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    Throttled,
)
from rest_framework.views import exception_handler


def safe_api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, Throttled):
        response.data = {"detail": "So'rovlar limiti tugadi. Birozdan so'ng qayta urinib ko'ring."}
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        response.data = {"detail": "Sessiya tugagan yoki kirish ma'lumotlari noto'g'ri."}
    elif isinstance(exc, NotFound):
        response.data = {"detail": "So'ralgan ma'lumot topilmadi."}
    return response
