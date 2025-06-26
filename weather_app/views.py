from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .consts import INSTALLATION_POWER_KW, PANEL_EFFICIENCY
from .utils.weather_utils import get_weekly_weather_data


class WeeklyDataView(APIView):
    def get(self, request):
        try:
            data = get_weekly_weather_data(request)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        if data is None:
            return Response(
                {"error": "Couldn't get data from api-open-meteo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = []
        for i in range(len(data["time"])):
            sunshine_hours = data["sunshine_duration"][i] / 3600
            energy_kwh = INSTALLATION_POWER_KW * sunshine_hours * PANEL_EFFICIENCY
            results.append(
                {
                    "date": data["time"][i],
                    "weather_code": data["weathercode"][i],
                    "temp_min": data["temperature_2m_min"][i],
                    "temp_max": data["temperature_2m_max"][i],
                    "estimated_energy": energy_kwh,
                }
            )
        return Response(results, status=status.HTTP_200_OK)


class WeeklySummaryView(APIView):
    def get(self, request):
        try:
            data = get_weekly_weather_data(request)
        except serializers.ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        if data is None:
            return Response(
                {"error": "Couldn't get data from api-open-meteo"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response("Summary", status=status.HTTP_200_OK)
