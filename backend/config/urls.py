from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import FileResponse, Http404
from django.urls import include, path, re_path


def serve_frontend(request, path=""):
    index_path = Path(settings.BASE_DIR) / "static" / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(index_path.open("rb"))
    raise Http404("Frontend build not found. Run npm install && npm run build before deployment.")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/ai/", include("apps.ai.urls")),
    path("api/planner/", include("apps.planner.urls")),
    path("api/", include("apps.services.urls")),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    re_path(r"^(?!api/|admin/|media/|static/).*", serve_frontend, name="frontend-index"),
]
