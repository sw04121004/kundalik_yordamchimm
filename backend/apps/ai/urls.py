from django.urls import path

from .views import (
    ConversationDetailView,
    ConversationListCreateView,
    PurposeListView,
    SendMessageView,
)

urlpatterns = [
    path("purposes/", PurposeListView.as_view(), name="ai-purposes"),
    path("conversations/", ConversationListCreateView.as_view(), name="ai-conversation-list"),
    path("conversations/<int:pk>/", ConversationDetailView.as_view(), name="ai-conversation-detail"),
    path("conversations/<int:pk>/messages/", SendMessageView.as_view(), name="ai-send-message"),
]
