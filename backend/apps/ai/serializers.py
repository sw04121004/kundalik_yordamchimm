from rest_framework import serializers

from .models import Conversation, Message, PURPOSE_CHOICES

VALID_PURPOSES = [choice[0] for choice in PURPOSE_CHOICES]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "role", "content", "created_at", "media_type", "media_url")
        read_only_fields = ("id", "role", "created_at", "media_type", "media_url")


class ConversationListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "title", "purpose", "created_at", "updated_at", "last_message")

    def get_last_message(self, obj):
        last = obj.messages.order_by("-created_at").first()
        if not last:
            return None
        text = last.content.strip()
        return text[:90] + ("…" if len(text) > 90 else "")


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ("id", "title", "purpose", "created_at", "updated_at", "messages")


def _get_lang_from_context(context):
    request = context.get("request") if context else None
    if not request:
        return "uz"
    accept = getattr(request, "headers", {}).get("Accept-Language", "uz") if hasattr(request, "headers") else request.META.get("HTTP_ACCEPT_LANGUAGE", "uz")
    lang = accept.split(",", 1)[0].split("-", 1)[0].lower()
    return lang if lang in ("uz", "ru", "en") else "uz"


_AI_MESSAGES = {
    "invalid_purpose": {
        "uz": "Noto'g'ri maqsad tanlandi.",
        "ru": "Выбрана неверная цель.",
        "en": "Invalid purpose selected.",
    },
    "empty_content": {
        "uz": "Xabar bo'sh bo'lishi mumkin emas.",
        "ru": "Сообщение не может быть пустым.",
        "en": "Message cannot be empty.",
    },
}


class ConversationCreateSerializer(serializers.ModelSerializer):
    purpose = serializers.CharField(max_length=50, default="general")

    class Meta:
        model = Conversation
        fields = ("id", "title", "purpose", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_purpose(self, value):
        if value not in VALID_PURPOSES:
            lang = _get_lang_from_context(self.context)
            raise serializers.ValidationError(_AI_MESSAGES["invalid_purpose"][lang])
        return value


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=4000, trim_whitespace=True)

    def validate_content(self, value):
        if not value or not value.strip():
            lang = _get_lang_from_context(self.context)
            raise serializers.ValidationError(_AI_MESSAGES["empty_content"][lang])
        return value.strip()
