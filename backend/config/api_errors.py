from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    Throttled,
)
from rest_framework.views import exception_handler


def _get_lang(context):
    request = context.get("request") if context else None
    if not request:
        return "uz"
    accept = getattr(request, "headers", {}).get("Accept-Language", "uz") if hasattr(request, "headers") else request.META.get("HTTP_ACCEPT_LANGUAGE", "uz")
    lang = accept.split(",", 1)[0].split("-", 1)[0].lower()
    return lang if lang in ("uz", "ru", "en") else "uz"


_MESSAGES = {
    "throttled": {
        "uz": "So'rovlar limiti tugadi. Birozdan so'ng qayta urinib ko'ring.",
        "ru": "Превышен лимит запросов. Пожалуйста, повторите попытку позже.",
        "en": "Rate limit exceeded. Please try again later.",
    },
    "auth": {
        "uz": "Sessiya tugagan yoki kirish ma'lumotlari noto'g'ri.",
        "ru": "Сессия истекла или неверные данные для входа.",
        "en": "Session expired or invalid credentials.",
    },
    "not_found": {
        "uz": "So'ralgan ma'lumot topilmadi.",
        "ru": "Запрашиваемые данные не найдены.",
        "en": "The requested data was not found.",
    },
}


def safe_api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    lang = _get_lang(context)

    if isinstance(exc, Throttled):
        response.data = {"detail": _MESSAGES["throttled"][lang]}
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        response.data = {"detail": _MESSAGES["auth"][lang]}
    elif isinstance(exc, NotFound):
        response.data = {"detail": _MESSAGES["not_found"][lang]}
    return response
