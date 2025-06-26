from ..serializers import LongitudeLatitudeSerializer
from ..services import WeatherService


def get_weekly_weather_data(request):
    lat_lot_serializer = LongitudeLatitudeSerializer(data=request.data)
    lat_lot_serializer.is_valid(raise_exception=True)

    data = WeatherService.get_weather(
        lat_lot_serializer.validated_data["latitude"],
        lat_lot_serializer.validated_data["longitude"],
    )

    return data
