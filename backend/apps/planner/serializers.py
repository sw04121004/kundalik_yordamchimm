from rest_framework import serializers

from .models import Task


def _get_lang_from_context(context):
    request = context.get("request") if context else None
    if not request:
        return "uz"
    accept = getattr(request, "headers", {}).get("Accept-Language", "uz") if hasattr(request, "headers") else request.META.get("HTTP_ACCEPT_LANGUAGE", "uz")
    lang = accept.split(",", 1)[0].split("-", 1)[0].lower()
    return lang if lang in ("uz", "ru", "en") else "uz"


_TITLE_EMPTY_MESSAGES = {
    "uz": "Vazifa nomi bo'sh bo'lishi mumkin emas.",
    "ru": "Название задачи не может быть пустым.",
    "en": "Task title cannot be empty.",
}


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "due_date", "due_time", "is_done", "created_at")
        read_only_fields = ("id", "created_at")
        extra_kwargs = {"title": {"allow_blank": True}}

    def validate_title(self, value):
        if not value or not value.strip():
            lang = _get_lang_from_context(self.context)
            raise serializers.ValidationError(_TITLE_EMPTY_MESSAGES[lang])
        return value.strip()
