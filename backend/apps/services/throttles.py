from rest_framework.throttling import UserRateThrottle


class WeatherSearchThrottle(UserRateThrottle):
    scope = "weather_search"


class WeatherForecastThrottle(UserRateThrottle):
    scope = "weather_forecast"
