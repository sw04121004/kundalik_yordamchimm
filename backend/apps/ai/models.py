from django.conf import settings
from django.db import models

PURPOSE_CHOICES = [
    ("general", "Umumiy AI"),
    ("kitchen", "Oshxona AI"),
    ("study", "O'qish AI"),
    ("document", "Hujjat AI"),
    ("translation", "Tarjima AI"),
    ("home", "Uy AI"),
    ("finance", "Moliya AI"),
    ("programming", "Kod AI"),
    ("ideas", "G'oya AI"),
    ("cv", "CV / Ish AI"),
]

ROLE_CHOICES = [
    ("user", "user"),
    ("assistant", "assistant"),
]


class Conversation(models.Model):
    """
    A single AI chat thread. Always scoped to one user — ownership is
    enforced in the views (querysets are always filtered by request.user),
    never only hidden in the frontend.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="ai_conversations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150, default="Yangi suhbat")
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default="general")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} ({self.user})"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"
