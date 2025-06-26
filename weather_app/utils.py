from datetime import datetime
from zoneinfo import ZoneInfo

from timezonefinder import TimezoneFinder

timezone_finder = TimezoneFinder()


def get_timezone(lat, lng):
    return timezone_finder.timezone_at(lat=lat, lng=lng)


def get_timezone_time(tz_name):
    return datetime.now(ZoneInfo(tz_name))
