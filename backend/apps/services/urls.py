from django.urls import path

from .views import (
    CategoryListView,
    FavoriteDeleteView,
    FavoriteListCreateView,
    ServiceListView,
    StatsView,
    UsageLogListCreateView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("usage/", UsageLogListCreateView.as_view(), name="usage-list-create"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("favorites/", FavoriteListCreateView.as_view(), name="favorite-list-create"),
    path("favorites/<slug:slug>/", FavoriteDeleteView.as_view(), name="favorite-delete"),
]
