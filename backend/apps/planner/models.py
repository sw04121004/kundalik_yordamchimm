from django.conf import settings
from django.db import models


class Task(models.Model):
    """
    A single to-do item. due_date/due_time are optional so a task can be a
    plain "someday" item or a scheduled one (used for the "Bugungi reja" /
    daily plan widget on the dashboard).
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "due_time", "created_at"]

    def __str__(self):
        return f"{self.title} ({self.user})"
