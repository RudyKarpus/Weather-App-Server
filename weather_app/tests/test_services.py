from unittest.mock import MagicMock, patch

import requests
from django.core.cache import cache
from django.test import TestCase

from weather_app.services import WeatherService


class WeatherServiceTest(TestCase):
    def setUp(self):
        self.latitude = 52.23
        self.longitude = 21.01
        self.cache_key = f"weather-{self.latitude}-{self.longitude}"

    def tearDown(self):
        cache.clear()

    @patch("weather_app.services.cache.get")
    def test_returns_cached_data(self, mock_cache_get):
        mock_data = {"mock": "cached"}
        mock_cache_get.return_value = mock_data

        result = WeatherService.get_weather(self.latitude, self.longitude)

        self.assertEqual(result, mock_data)
        mock_cache_get.assert_called_once_with(self.cache_key)

    @patch("weather_app.services.get_timezone")
    @patch("weather_app.services.requests.get")
    @patch("weather_app.services.get_timezone_time")
    @patch("weather_app.services.cache.set")
    @patch("weather_app.services.cache.get", return_value=None)
    def test_fetches_data_when_not_cached(
        self,
        mock_cache_get,
        mock_cache_set,
        mock_get_timezone_time,
        mock_requests_get,
        mock_get_timezone,
    ):
        mock_response = MagicMock()
        mock_response.json.return_value = {"daily": {"temp": [20, 21]}}
        mock_requests_get.return_value = mock_response
        mock_get_timezone.return_value = "Europe/Warsaw"

        from datetime import datetime as dt
        from datetime import timezone

        mock_time = dt(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_get_timezone_time.return_value = mock_time

        result = WeatherService.get_weather(self.latitude, self.longitude)

        self.assertEqual(result, {"temp": [20, 21]})
        mock_get_timezone.assert_called_once_with(self.latitude, self.longitude)
        mock_requests_get.assert_called_once()
        mock_cache_set.assert_called_once()
        mock_get_timezone_time.assert_called_once_with("Europe/Warsaw")

    @patch(
        "weather_app.services.requests.get",
        side_effect=requests.RequestException("fail"),
    )
    @patch("weather_app.services.get_timezone")
    @patch("weather_app.services.cache.get", return_value=None)
    def test_handles_api_failure(
        self, mock_cache_get, mock_get_timezone, mock_requests_get
    ):
        mock_get_timezone.return_value = "Europe/Warsaw"

        result = WeatherService.get_weather(self.latitude, self.longitude)

        self.assertIsNone(result)
        mock_requests_get.assert_called_once()
