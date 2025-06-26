from datetime import datetime, time

import requests
from django.core.cache import cache

from .utils.time_utils import get_timezone, get_timezone_time


class WeatherService:
    @staticmethod
    def get_weather(latitude, longitude):
        cache_key = f"weather-{latitude}-{longitude}"
        data = cache.get(cache_key)

        if not data:
            url = "https://api.open-meteo.com/v1/forecast"
            time_zone = get_timezone(latitude, longitude)
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "weathercode",
                    "sunshine_duration",
                    "surface_pressure_mean",
                ],
                "timezone": time_zone,
            }
            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json().get("daily", {})
            except requests.RequestException as e:
                print("WeatherService: Couldn't get data from api", e)
                return None
            # Calculate cache time
            tz_time = get_timezone_time(time_zone)
            midnight = datetime.combine(
                tz_time.date(), time(23, 59, 59, 9), tzinfo=tz_time.tzinfo
            )
            seconds_to_midnight = int((midnight - tz_time).total_seconds())

            cache.set(cache_key, data, seconds_to_midnight)
        return data
