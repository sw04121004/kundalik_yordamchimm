from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Favorite, Service, UsageLog
from .serializers import (
    CategorySerializer,
    FavoriteSerializer,
    ServiceSerializer,
    UsageLogSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related("services").all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ]
    ordering_fields = ["name", "order"]
    pagination_class = None  # uses default PAGE_SIZE from settings

    def get_queryset(self):
        qs = Service.objects.select_related("category").all()
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class UsageLogListCreateView(generics.ListCreateAPIView):
    serializer_class = UsageLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            UsageLog.objects.filter(user=self.request.user)
            .select_related("service")[:20]
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total = UsageLog.objects.filter(user=request.user).count()
        return Response({"total_usage": total})


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("service")

    def create(self, request, *args, **kwargs):
        service_slug = request.data.get("service_slug")
        service = get_object_or_404(Service, slug=service_slug)
        favorite, _ = Favorite.objects.get_or_create(user=request.user, service=service)
        return Response(FavoriteSerializer(favorite).data, status=201)


class FavoriteDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, slug):
        deleted, _ = Favorite.objects.filter(user=request.user, service__slug=slug).delete()
        if not deleted:
            return Response({"detail": "Sevimli topilmadi."}, status=404)
        return Response(status=204)
