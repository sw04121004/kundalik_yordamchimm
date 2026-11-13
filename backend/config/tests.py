from unittest.mock import patch

from django.db import OperationalError
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from .startup import verify_production_database


class HealthCheckTests(SimpleTestCase):
    @patch("config.health.verify_database_connection")
    def test_health_check_returns_ok_when_database_query_succeeds(self, verify_database):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})
        verify_database.assert_called_once_with()

    @patch("config.health.verify_database_connection", side_effect=OperationalError("private db detail"))
    def test_health_check_does_not_expose_database_error(self, _verify_database):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"status": "unavailable", "database": "unavailable"},
        )
        self.assertNotIn(b"private db detail", response.content)


class ProductionStartupTests(SimpleTestCase):
    @override_settings(DEBUG=False)
    @patch("config.startup.connection")
    def test_unavailable_database_fails_with_actionable_message(self, db_connection):
        db_connection.cursor.side_effect = OperationalError("private database details")
        with self.assertRaisesRegex(RuntimeError, "database could not be reached") as raised:
            verify_production_database()

        self.assertIn("connect timeout is 10 seconds", str(raised.exception))
        self.assertNotIn("private database details", str(raised.exception))

    @override_settings(DEBUG=True)
    @patch("config.startup.connection")
    def test_local_debug_does_not_probe_database_at_wsgi_startup(self, db_connection):
        verify_production_database()
        db_connection.cursor.assert_not_called()
