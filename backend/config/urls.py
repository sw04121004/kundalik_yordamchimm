from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/ai/", include("apps.ai.urls")),
    path("api/planner/", include("apps.planner.urls")),
    path("api/", include("apps.services.urls")),
]
