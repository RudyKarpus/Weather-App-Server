import requests

from .utils.time_utils import get_timezone


class WeatherService:
    """Service getting weekly weatcher data

    Args:
        latitude: geographical latitude
        longitude: geographical longitude

    Returns:
        Data from meto Api

    """

    @staticmethod
    def get_weather(latitude, longitude):
        """
        Checks wether weather was already checked and cached or gets weather from api
        """
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

        return data
