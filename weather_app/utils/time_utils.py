from datetime import datetime
from zoneinfo import ZoneInfo

from timezonefinder import TimezoneFinder

timezone_finder = TimezoneFinder()


def get_timezone(lat, lng):
    """Utils method for getting time zone

    Args:
        lat: geographical latitude
        lng: geographical longitude

    Returns:
        Time zone name
    """
    return timezone_finder.timezone_at(lat=lat, lng=lng)


def get_timezone_time(tz_name):
    """Utils method for getting timezone's time

    Args:
        tz_name: name of timezone

    Returns:
        datetime time
    """
    return datetime.now(ZoneInfo(tz_name))
