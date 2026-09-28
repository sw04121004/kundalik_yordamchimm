from rest_framework import serializers
from .models import Category, Favorite, Service, UsageLog, Transaction


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "route",
            "order",
            "category",
            "category_name",
        )


class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon", "description", "order", "services")


class FavoriteSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "service", "created_at")
        read_only_fields = ("id", "created_at", "user")


class UsageLogSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    service_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Service.objects.all(),
        source="service",
    )

    class Meta:
        model = UsageLog
        fields = ("id", "service_slug", "service_name", "created_at")
        read_only_fields = ("id", "created_at", "user", "service")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "type", "amount", "category", "description", "date", "created_at")
        read_only_fields = ("id", "created_at", "user")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)