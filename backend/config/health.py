from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


def verify_database_connection():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")


@require_GET
def health_check(request):
    try:
        verify_database_connection()
    except DatabaseError:
        return JsonResponse(
            {"status": "unavailable", "database": "unavailable"},
            status=503,
        )

    return JsonResponse({"status": "ok", "database": "ok"})
