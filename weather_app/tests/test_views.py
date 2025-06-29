from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from weather_app.views import INSTALLATION_POWER_KW, PANEL_EFFICIENCY


class WeeklyDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            "weekly_data", kwargs={"latitude": "52.23", "longitude": "21.01"}
        )
        self.mock_data = {
            "time": ["2024-01-01", "2024-01-02"],
            "weathercode": [1, 2],
            "temperature_2m_min": [1.1, 2.2],
            "temperature_2m_max": [5.5, 6.6],
            "sunshine_duration": [3600, 7200],
        }

    @patch("weather_app.views.get_weekly_weather_data")
    def test_successful_data_fetch(self, mock_get_data):
        mock_get_data.return_value = self.mock_data

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertAlmostEqual(
            response.data[0]["estimated_energy"],
            INSTALLATION_POWER_KW * (3600 / 3600) * PANEL_EFFICIENCY,
        )

    @patch("weather_app.views.get_weekly_weather_data")
    def test_api_returns_none(self, mock_get_data):
        mock_get_data.return_value = None

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch("weather_app.views.get_weekly_weather_data")
    def test_invalid_lat_lon_data(self, mock_get_data):
        from rest_framework import serializers

        mock_get_data.side_effect = serializers.ValidationError(
            {"error": "invalid input"}
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class WeeklySummaryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            "weekly_summary", kwargs={"latitude": "52.23", "longitude": "21.01"}
        )
        self.mock_data = {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "weathercode": [1, 2, 3],
            "temperature_2m_min": [1.1, 2.2, 0.9],
            "temperature_2m_max": [5.5, 6.6, 7.1],
            "sunshine_duration": [3600, 7200, 10800],
            "surface_pressure_mean": [1012, 1015, 1018],
        }

    @patch("weather_app.views.get_weekly_weather_data")
    @patch("weather_app.views.summarize_weather")
    def test_successful_summary(self, mock_summary, mock_get_data):
        mock_get_data.return_value = self.mock_data
        mock_summary.return_value = "Mixed weather with some sun and clouds"

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("average_pressure", response.data)
        self.assertEqual(response.data["min_temperature"], 0.9)
        self.assertEqual(response.data["max_temperature"], 7.1)
        self.assertIn("weekly_summary", response.data)

    @patch("weather_app.views.get_weekly_weather_data")
    def test_summary_api_returns_none(self, mock_get_data):
        mock_get_data.return_value = None

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("weather_app.views.get_weekly_weather_data")
    def test_summary_invalid_data(self, mock_get_data):
        from rest_framework import serializers

        mock_get_data.side_effect = serializers.ValidationError(
            {"error": "invalid input"}
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
