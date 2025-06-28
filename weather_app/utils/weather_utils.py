from collections import Counter

from ..consts import CODE_CATEGORY_TO_VERB, WMO_CODE_CATEGORY
from ..serializers import LongitudeLatitudeSerializer
from ..services import WeatherService


def get_weekly_weather_data(input_data):
    """Method used accross views to acces WeatherData

    Args:
        input_data: dict with latitude and longitude

    Returns:
        Data from meto Api
    """
    lat_lot_serializer = LongitudeLatitudeSerializer(data=input_data)
    lat_lot_serializer.is_valid(raise_exception=True)

    data = WeatherService.get_weather(
        lat_lot_serializer.validated_data["latitude"],
        lat_lot_serializer.validated_data["longitude"],
    )

    return data


def summarize_weather(codes):
    """Utils method for generating weather summary

    Args:
        code: list of WMO weather codes

    Returns:
        String summarazing weather
    """
    categories = [WMO_CODE_CATEGORY.get(code) for code in codes]
    count = Counter(categories)

    # Sort by frequency
    most_common = [cat for cat, _ in count.most_common()]

    summary = []

    if most_common:
        main_weather = most_common[0]
        summary.append(f"Mostly {main_weather}")

        n = 0
        # add to summary secondary occuring weather
        for weather in most_common[1:]:
            word = CODE_CATEGORY_TO_VERB.get(weather, weather)
            if n == 0:
                summary.append(f"and it will be {word}")
                n = weather[1]
            elif n == weather[1]:
                summary.append(f", {word}")
            else:
                break
    else:
        summary.append("Weather data unavailable")

    return " ".join(summary)
