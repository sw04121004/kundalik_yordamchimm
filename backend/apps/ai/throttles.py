from rest_framework.throttling import UserRateThrottle


class AIRequestMinuteThrottle(UserRateThrottle):
    scope = "ai_per_minute"


class AIRequestDailyThrottle(UserRateThrottle):
    scope = "ai_per_day"
