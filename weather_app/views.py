from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .consts import INSTALLATION_POWER_KW, PANEL_EFFICIENCY
from .serializers import LongitudeLatitudeSerializer
from .services import WeatherService


class WeeklyDataView(APIView):
    def get(self, request):

        lat_lot_serializer = LongitudeLatitudeSerializer(data=request.data)
        if not lat_lot_serializer.is_valid(raise_exception=True):
            return Response(
                lat_lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = WeatherService.get_weather(
            lat_lot_serializer.validated_data["latitude"],
            lat_lot_serializer.validated_data["longitude"],
        )

        if data is None:
            return Response(
                "Couldn't get data from api-open-meteo",
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
        return Response("Summary", status=status.HTTP_200_OK)
