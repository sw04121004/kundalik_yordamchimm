from datetime import date, timedelta
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .throttles import WeatherSearchThrottle


User = get_user_model()


class WeatherEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="weather-user", password="StrongPass123!")

    def test_weather_endpoints_require_authentication(self):
        self.assertEqual(
            self.client.get(reverse("weather-search"), {"q": "Tashkent"}).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            self.client.get(reverse("weather-forecast"), {"lat": 41.3, "lon": 69.2}).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("apps.services.weather.requests.get")
    def test_location_search_maps_provider_results_and_applies_country_filter(self, get):
        cache.clear()
        provider_response = Mock()
        provider_response.raise_for_status.return_value = None
        provider_response.json.return_value = {"results": [{
            "name": "Toshkent", "admin1": "Toshkent shahri", "country": "O'zbekiston",
            "country_code": "UZ", "latitude": 41.3111, "longitude": 69.2797,
        }]}
        get.return_value = provider_response
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse("weather-search"), {"q": "Toshkent", "country": "uz", "lang": "uz"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], {
            "name": "Toshkent", "admin1": "Toshkent shahri", "country": "O'zbekiston",
            "country_code": "UZ", "lat": 41.3111, "lon": 69.2797,
        })
        request = get.call_args
        self.assertEqual(request.kwargs["timeout"], 8)
        self.assertEqual(request.kwargs["params"]["count"], 8)
        self.assertEqual(request.kwargs["params"]["countryCode"], "UZ")
        self.assertIn("geocoding-api.open-meteo.com", request.args[0])

    @patch("apps.services.weather.requests.get")
    def test_search_endpoint_is_throttled_per_user(self, get):
        cache.clear()
        provider_response = Mock()
        provider_response.raise_for_status.return_value = None
        provider_response.json.return_value = {"results": []}
        get.return_value = provider_response
        self.client.force_authenticate(self.user)
        rates = {**WeatherSearchThrottle.THROTTLE_RATES, "weather_search": "1/min"}

        with patch.object(WeatherSearchThrottle, "THROTTLE_RATES", rates):
            first = self.client.get(reverse("weather-search"), {"q": "London"})
            second = self.client.get(reverse("weather-search"), {"q": "Paris"})

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(get.call_count, 1)

    @patch("apps.services.weather.OPEN_METEO_API_KEY", "test-open-meteo-key")
    @patch("apps.services.weather.requests.get")
    def test_optional_key_uses_customer_geocoding_host(self, get):
        cache.clear()
        provider_response = Mock()
        provider_response.raise_for_status.return_value = None
        provider_response.json.return_value = {"results": []}
        get.return_value = provider_response
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("weather-search"), {"q": "London"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("customer-geocoding-api.open-meteo.com", get.call_args.args[0])
        self.assertEqual(get.call_args.kwargs["params"]["apikey"], "test-open-meteo-key")

    @patch("apps.services.weather.requests.get")
    def test_forecast_returns_current_24_hours_and_14_days_and_is_cached(self, get):
        cache.clear()
        start = date(2026, 11, 13)
        hours = [f"2026-11-13T{hour:02d}:00" for hour in range(24)]
        hours += [f"2026-11-14T{hour:02d}:00" for hour in range(8)]
        days = [(start + timedelta(days=offset)).isoformat() for offset in range(14)]
        payload = {
            "timezone": "Asia/Tashkent",
            "current": {
                "time": "2026-11-13T08:00", "temperature_2m": 18, "apparent_temperature": 17,
                "relative_humidity_2m": 45, "wind_speed_10m": 8, "precipitation": 0,
                "surface_pressure": 1012, "weather_code": 2, "is_day": 1,
            },
            "current_units": {
                "temperature_2m": "°C", "wind_speed_10m": "km/h",
                "precipitation": "mm", "surface_pressure": "hPa",
            },
            "hourly": {
                "time": hours, "temperature_2m": list(range(len(hours))),
                "precipitation_probability": [0] * len(hours), "weather_code": [2] * len(hours),
            },
            "daily": {
                "time": days, "weather_code": [2] * 14, "temperature_2m_max": [22] * 14,
                "temperature_2m_min": [10] * 14, "precipitation_sum": [0] * 14,
                "precipitation_probability_max": [5] * 14, "wind_speed_10m_max": [12] * 14,
                "sunrise": ["06:00"] * 14, "sunset": ["18:00"] * 14,
            },
        }
        provider_response = Mock()
        provider_response.raise_for_status.return_value = None
        provider_response.json.return_value = payload
        get.return_value = provider_response
        self.client.force_authenticate(self.user)
        url = reverse("weather-forecast")

        first = self.client.get(url, {"lat": "41.3111", "lon": "69.2797", "lang": "uz"})
        second = self.client.get(url, {"lat": "41.312", "lon": "69.276", "lang": "ru"})

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(len(first.data["hourly"]), 24)
        self.assertEqual(first.data["hourly"][0]["time"], "2026-11-13T08:00")
        self.assertEqual(len(first.data["daily"]), 14)
        self.assertEqual(first.data["current"]["apparent_temperature"], 17)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(get.call_count, 1)
        self.assertEqual(get.call_args.kwargs["timeout"], 8)
        self.assertEqual(get.call_args.kwargs["params"]["forecast_days"], 14)
        self.assertEqual(get.call_args.kwargs["params"]["timezone"], "auto")

    @patch("apps.services.weather.requests.get", side_effect=TimeoutError("private provider detail"))
    def test_provider_failure_is_clear_and_does_not_leak_provider_error(self, _get):
        cache.clear()
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("weather-forecast"), {"lat": 41, "lon": 69})

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn("Ob-havo xizmati", response.data["detail"])
        self.assertNotIn("private provider detail", str(response.data))

    def test_forecast_rejects_out_of_range_coordinates(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("weather-forecast"), {"lat": 91, "lon": 69})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("lat", response.data)

    @patch("apps.services.weather.requests.get")
    def test_geocoding_accepts_additional_two_letter_language(self, get):
        cache.clear()
        provider_response = Mock()
        provider_response.raise_for_status.return_value = None
        provider_response.json.return_value = {"results": []}
        get.return_value = provider_response
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("weather-search"), {"q": "Paris", "lang": "fr"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get.call_args.kwargs["params"]["language"], "fr")
