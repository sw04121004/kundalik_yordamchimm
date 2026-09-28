from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, PURPOSE_CHOICES
from .serializers import (
    ConversationCreateSerializer,
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
    SendMessageSerializer,
)
from .services import AIUnavailableError, generate_reply, is_configured


class PurposeListView(APIView):
    """Public list of AI purposes the frontend can render as a picker."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response([{"value": value, "label": label} for value, label in PURPOSE_CHOICES])


class ConversationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # SECURITY: always scoped to the authenticated user. A user can only
        # ever see their own conversations — this is enforced here, at the
        # database query level, not just hidden in the UI.
        return Conversation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ConversationCreateSerializer
        return ConversationListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConversationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ConversationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # SECURITY: same scoping as above — a 404 is returned (not a 403)
        # for another user's conversation id, so existence isn't leaked.
        return Conversation.objects.filter(user=self.request.user)


class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # Accept JSON or multipart form data (for file uploads)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk, user=request.user)

        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data["content"]

        # ----- Media handling -----
        media_file = request.FILES.get("media")
        media_type = None
        media_url = None
        if media_file:
            # Determine a simple media_type string
            ct = media_file.content_type
            if ct.startswith("image/"):
                media_type = "image"
            elif ct.startswith("video/"):
                media_type = "video"
            elif ct.startswith("audio/"):
                media_type = "audio"
            else:
                media_type = "file"

            # Save the file and obtain a public URL
            from .storage import save_media
            media_url = save_media(media_file)

        # Create the user's message, including media info if present
        user_message = Message.objects.create(
            conversation=conversation,
            role="user",
            content=content,
            media_type=media_type,
            media_url=media_url,
        )

        if conversation.messages.count() == 1:
            conversation.title = (content[:40] + "…") if len(content) > 40 else content

        history = [
            {"role": message.role, "content": message.content}
            for message in conversation.messages.order_by("created_at")
        ]

        ai_ok = True
        try:
            reply_text = generate_reply(conversation.purpose, history)
        except AIUnavailableError as exc:
            reply_text = f"😔 Xatolik yuz berdi: {str(exc)}"
            ai_ok = False

        assistant_message = Message.objects.create(
            conversation=conversation, role="assistant", content=reply_text
        )

        # bump updated_at (auto_now) and persist any title change above
        conversation.save()

        return Response(
            {
                "user_message": MessageSerializer(user_message).data,
                "assistant_message": MessageSerializer(assistant_message).data,
                "conversation_title": conversation.title,
                "ai_configured": is_configured(),
                "ai_ok": ai_ok,
            },
            status=status.HTTP_201_CREATED,
        )
