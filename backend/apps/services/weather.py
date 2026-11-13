import os

import requests
from django.core.cache import cache
from rest_framework.exceptions import APIException


CACHE_SECONDS = 10 * 60
REQUEST_TIMEOUT_SECONDS = 8
OPEN_METEO_API_KEY = os.environ.get("OPEN_METEO_API_KEY", "").strip()


class WeatherProviderError(APIException):
    status_code = 503
    default_detail = "Ob-havo xizmati vaqtincha ishlamayapti. Keyinroq qayta urinib ko'ring."
    default_code = "weather_provider_unavailable"


def _provider_url(resource):
    if OPEN_METEO_API_KEY:
        if resource == "geocoding":
            return "https://customer-geocoding-api.open-meteo.com/v1/search"
        return "https://customer-api.open-meteo.com/v1/forecast"
    if resource == "geocoding":
        return "https://geocoding-api.open-meteo.com/v1/search"
    return "https://api.open-meteo.com/v1/forecast"


def _get_json(resource, params):
    params = dict(params)
    if OPEN_METEO_API_KEY:
        params["apikey"] = OPEN_METEO_API_KEY
    try:
        response = requests.get(
            _provider_url(resource), params=params, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, TimeoutError, ValueError):
        raise WeatherProviderError() from None

    if not isinstance(payload, dict) or payload.get("error"):
        raise WeatherProviderError()
    return payload


def search_locations(query, country_code="", language="uz"):
    normalized = query.strip()
    cache_key = f"weather:search:{language}:{country_code.upper()}:{normalized.casefold()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    params = {"name": normalized, "count": 8, "language": language, "format": "json"}
    if country_code:
        params["countryCode"] = country_code.upper()
    payload = _get_json("geocoding", params)
    locations = [
        {
            "name": result.get("name", ""),
            "admin1": result.get("admin1", ""),
            "country": result.get("country", ""),
            "country_code": result.get("country_code", ""),
            "lat": result.get("latitude"),
            "lon": result.get("longitude"),
        }
        for result in payload.get("results", [])
        if isinstance(result, dict)
    ]
    cache.set(cache_key, locations, CACHE_SECONDS)
    return locations


def get_forecast(latitude, longitude):
    lat_key = round(float(latitude), 2)
    lon_key = round(float(longitude), 2)
    cache_key = f"weather:forecast:{lat_key:.2f}:{lon_key:.2f}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    payload = _get_json(
        "forecast",
        {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "forecast_days": 14,
            "current": ",".join(
                (
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "wind_speed_10m",
                    "precipitation",
                    "surface_pressure",
                    "weather_code",
                    "is_day",
                )
            ),
            "hourly": "temperature_2m,precipitation_probability,weather_code",
            "daily": ",".join(
                (
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "precipitation_probability_max",
                    "wind_speed_10m_max",
                    "sunrise",
                    "sunset",
                )
            ),
        },
    )

    current_data = payload.get("current", {})
    current = {
        "time": current_data.get("time"),
        "temperature": current_data.get("temperature_2m"),
        "apparent_temperature": current_data.get("apparent_temperature"),
        "humidity": current_data.get("relative_humidity_2m"),
        "wind_speed": current_data.get("wind_speed_10m"),
        "precipitation": current_data.get("precipitation"),
        "pressure": current_data.get("surface_pressure"),
        "weather_code": current_data.get("weather_code"),
        "is_day": current_data.get("is_day") == 1,
    }

    hourly_data = payload.get("hourly", {})
    hourly_times = hourly_data.get("time", [])
    start_at = next(
        (index for index, hour in enumerate(hourly_times) if hour >= (current["time"] or "")),
        0,
    )
    hourly = [
        {
            "time": hour,
            "temperature": hourly_data.get("temperature_2m", [None] * len(hourly_times))[index],
            "precipitation_probability": hourly_data.get("precipitation_probability", [None] * len(hourly_times))[index],
            "weather_code": hourly_data.get("weather_code", [None] * len(hourly_times))[index],
        }
        for index, hour in enumerate(hourly_times[start_at : start_at + 24], start=start_at)
    ]

    daily_data = payload.get("daily", {})
    daily = [
        {
            "date": day,
            "weather_code": daily_data.get("weather_code", [None] * len(daily_data.get("time", [])))[index],
            "temperature_max": daily_data.get("temperature_2m_max", [None] * len(daily_data["time"]))[index],
            "temperature_min": daily_data.get("temperature_2m_min", [None] * len(daily_data["time"]))[index],
            "precipitation_sum": daily_data.get("precipitation_sum", [None] * len(daily_data["time"]))[index],
            "precipitation_probability": daily_data.get("precipitation_probability_max", [None] * len(daily_data["time"]))[index],
            "wind_speed_max": daily_data.get("wind_speed_10m_max", [None] * len(daily_data["time"]))[index],
            "sunrise": daily_data.get("sunrise", [None] * len(daily_data["time"]))[index],
            "sunset": daily_data.get("sunset", [None] * len(daily_data["time"]))[index],
        }
        for index, day in enumerate(daily_data.get("time", []))
    ]

    result = {
        "current": current,
        "hourly": hourly,
        "daily": daily,
        "timezone": payload.get("timezone", "auto"),
        "units": {
            "temperature": payload.get("current_units", {}).get("temperature_2m", "°C"),
            "wind_speed": payload.get("current_units", {}).get("wind_speed_10m", "km/h"),
            "precipitation": payload.get("current_units", {}).get("precipitation", "mm"),
            "pressure": payload.get("current_units", {}).get("surface_pressure", "hPa"),
        },
    }
    cache.set(cache_key, result, CACHE_SECONDS)
    return result
