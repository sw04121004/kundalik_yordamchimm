from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default="🧩")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, related_name="services", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=10, default="⚙️")
    route = models.CharField(max_length=100, help_text="Frontend route path, e.g. /tools/percent")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class UsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="usage_logs", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="usage_logs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.service} @ {self.created_at:%Y-%m-%d %H:%M}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorites", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="favorited_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "service")

    def __str__(self):
        return f"{self.user} ♥ {self.service}"
