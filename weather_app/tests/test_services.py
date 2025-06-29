from unittest.mock import Mock, patch

from django.test import TestCase

from weather_app.services import WeatherService


class WeatherServiceTest(TestCase):

    @patch("weather_app.services.get_timezone")
    @patch("weather_app.services.requests.get")
    def test_get_weather_successful_response(
        self, mock_requests_get, mock_get_timezone
    ):
        mock_get_timezone.return_value = "Europe/Warsaw"

        mock_response = Mock()
        mock_response.json.return_value = {
            "daily": {"temperature_2m_max": [22, 23], "temperature_2m_min": [12, 13]}
        }
        mock_requests_get.return_value = mock_response

        latitude = 52.23
        longitude = 21.01

        result = WeatherService.get_weather(latitude, longitude)

        self.assertEqual(
            result,
            {
                "temperature_2m_max": [22, 23],
                "temperature_2m_min": [12, 13],
            },
        )
        mock_get_timezone.assert_called_once_with(latitude, longitude)
        mock_requests_get.assert_called_once()

    @patch("weather_app.services.get_timezone")
    @patch("weather_app.services.requests.get")
    def test_get_weather_empty_daily_fallback(
        self, mock_requests_get, mock_get_timezone
    ):
        mock_get_timezone.return_value = "Europe/Warsaw"
        mock_response = Mock()
        mock_response.json.return_value = {}  # Missing 'daily'
        mock_requests_get.return_value = mock_response

        result = WeatherService.get_weather(52.23, 21.01)

        self.assertEqual(result, {})  # Should return empty dict instead of None
