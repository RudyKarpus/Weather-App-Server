from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from weather_app.utils.weather_utils import get_weekly_weather_data, summarize_weather


class GetWeeklyWeatherDataTest(TestCase):
    def setUp(self):
        self.valid_input = {"latitude": 52.23, "longitude": 21.01}
        self.invalid_input = {"latitude": 999, "longitude": 999}

    @patch("weather_app.utils.weather_utils.WeatherService.get_weather")
    def test_valid_input_returns_data(self, mock_get_weather):
        mock_data = {"temp_max": [20, 21]}
        mock_get_weather.return_value = mock_data

        result = get_weekly_weather_data(self.valid_input)
        self.assertEqual(result, mock_data)
        mock_get_weather.assert_called_once_with(52.23, 21.01)

    def test_invalid_input_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            get_weekly_weather_data(self.invalid_input)


class SummarizeWeatherTest(TestCase):
    def test_summary_with_common_weather_codes(self):
        codes = [0, 0, 1, 1, 2, 45, 45]
        summary = summarize_weather(codes)
        self.assertTrue("Mostly" in summary)

    def test_summary_with_unknown_codes(self):
        codes = [999, 888]
        summary = summarize_weather(codes)
        self.assertIn("Mostly", summary)

    def test_empty_codes_returns_unavailable(self):
        summary = summarize_weather([])
        self.assertEqual(summary, "Weather data unavailable")
