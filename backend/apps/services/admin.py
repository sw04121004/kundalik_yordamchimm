from django.contrib import admin

from .models import Category, Favorite, Service, UsageLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "route", "order")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "created_at")
    list_filter = ("service",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "created_at")
