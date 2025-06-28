from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .consts import INSTALLATION_POWER_KW, PANEL_EFFICIENCY
from .utils.weather_utils import get_weekly_weather_data, summarize_weather


class WeeklyDataView(APIView):
    @swagger_auto_schema(
        tags=["Weather Data"],
        operation_description=(
            "Get weather weekly data" + "from meteoAPI based on latitude and longitude"
        ),
        manual_parameters=[
            openapi.Parameter(
                "latitude",
                openapi.IN_PATH,
                description="Latitude of location",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "longitude",
                openapi.IN_PATH,
                description="Longitude of location",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success response with fetched data",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "date": openapi.Schema(type=openapi.TYPE_STRING),
                            "weather_code": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "temp_min": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "temp_max": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "estimated_energy": openapi.Schema(
                                type=openapi.TYPE_NUMBER
                            ),
                        },
                    ),
                ),
            ),
            400: "Bad request",
        },
    )
    def get(self, request, latitude, longitude):
        input_data = {
            "latitude": latitude,
            "longitude": longitude,
        }
        try:
            data = get_weekly_weather_data(input_data)
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
    @swagger_auto_schema(
        tags=["Weather Data"],
        operation_description=(
            "Get weather weekly summary data"
            + "from meteoAPI based on latitude and longitude"
        ),
        manual_parameters=[
            openapi.Parameter(
                "latitude",
                openapi.IN_PATH,
                description="Latitude of location",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "longitude",
                openapi.IN_PATH,
                description="Longitude of location",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success response with fetched data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "average_pressure": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "average_sunshine_hours": openapi.Schema(
                            type=openapi.TYPE_NUMBER
                        ),
                        "min_temperature": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "max_temperature": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "weekly_summary": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Bad request",
        },
    )
    def get(self, request, latitude, longitude):
        input_data = {
            "latitude": latitude,
            "longitude": longitude,
        }
        try:
            data = get_weekly_weather_data(input_data)
        except serializers.ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        if data is None:
            return Response(
                {"error": "Couldn't get data from api-open-meteo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        count = len(data["time"])
        avg_pressure = sum(data["surface_pressure_mean"]) / count
        avg_sunshine = sum(data["sunshine_duration"]) / count
        avg_sunshine_hours = round(avg_sunshine / 3600, 2)
        min_temp = min(data["temperature_2m_min"])
        max_temp = max(data["temperature_2m_max"])
        summary = summarize_weather(data["weathercode"])

        response = {
            "average_pressure": round(avg_pressure, 2),
            "average_sunshine_hours": avg_sunshine_hours,
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "weekly_summary": summary,
        }

        return Response(response, status=status.HTTP_200_OK)
