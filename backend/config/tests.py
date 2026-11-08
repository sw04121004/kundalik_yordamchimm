from unittest.mock import patch

from django.db import OperationalError
from django.test import SimpleTestCase
from django.urls import reverse


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
