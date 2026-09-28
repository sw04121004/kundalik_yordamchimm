from django.urls import path

from .views import (CategoryListView,FavoriteDeleteView,FavoriteListCreateView,ServiceListView,StatsView,UsageLogListCreateView,TransactionListCreateView,TransactionRetrieveUpdateDestroyView)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("usage/", UsageLogListCreateView.as_view(), name="usage-list-create"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("favorites/", FavoriteListCreateView.as_view(), name="favorite-list-create"),
    path("favorites/<slug:slug>/", FavoriteDeleteView.as_view(), name="favorite-delete"),
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path("transactions/<int:pk>/", TransactionRetrieveUpdateDestroyView.as_view(), name="transaction-detail"),
]
