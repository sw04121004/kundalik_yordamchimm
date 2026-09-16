from rest_framework import serializers

from .models import Conversation, Message, PURPOSE_CHOICES

VALID_PURPOSES = [choice[0] for choice in PURPOSE_CHOICES]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "role", "content", "created_at")
        read_only_fields = ("id", "role", "created_at")


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


class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("id", "title", "purpose", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_purpose(self, value):
        if value not in VALID_PURPOSES:
            raise serializers.ValidationError("Noto'g'ri maqsad tanlandi.")
        return value


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=4000, trim_whitespace=True)

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Xabar bo'sh bo'lishi mumkin emas.")
        return value.strip()
