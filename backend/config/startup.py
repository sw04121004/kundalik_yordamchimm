from django.conf import settings
from django.db import connection


def verify_production_database():
    """Fail fast before serving traffic if the production database is unreachable."""
    if settings.DEBUG:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        raise RuntimeError(
            "Production startup failed: the database could not be reached. "
            "Check DATABASE_URL and database availability. PostgreSQL connect timeout is 10 seconds."
        ) from None
