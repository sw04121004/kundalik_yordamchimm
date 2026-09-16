from rest_framework import serializers

from .models import Category, Favorite, Service, UsageLog


class ServiceSerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = Service
        fields = ("id", "name", "slug", "description", "icon", "route", "category_slug")


class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon", "services")


class UsageLogSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_slug = serializers.SlugRelatedField(
        source="service", slug_field="slug", queryset=Service.objects.all(), write_only=True
    )

    class Meta:
        model = UsageLog
        fields = ("id", "service", "service_slug", "created_at")


class FavoriteSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_slug = serializers.SlugRelatedField(
        source="service", slug_field="slug", queryset=Service.objects.all(), write_only=True
    )

    class Meta:
        model = Favorite
        fields = ("id", "service", "service_slug", "created_at")
