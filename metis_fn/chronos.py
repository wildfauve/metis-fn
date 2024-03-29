from typing import Callable, List, Tuple
from dateutil.parser import parse as date_parser
from datetime import datetime, timedelta, timezone
from operator import methodcaller
from functools import reduce
from isoduration import parse_duration

import pendulum

from . import monad

@monad.Try()
def try_parse_iso8601_time(iso_str: str):
    return pendulum.parse(iso_str)


@monad.Try()
def try_parse_iso8601_duration(iso_str: str):
    return parse_duration(iso_str)


def time_now(tz: str = "UTC", apply: List[Callable] = None) -> datetime:
    """
    Generates Time now as a DateTime object without args.

    Add a TZ by providing a TZ arg:
    > time_now(tz=tz_utc)

    Call an addition functions on the datetime using the apply arg.
    + To format in iso8601, provide the iso8601 function
    > time_now(tz=tz_utc, apply=[iso8601()]
    """
    dt = pendulum.now(tz=tz)
    if apply is None:
        return dt
    return apply_appliers(dt, apply)

def tz_convert(time, zone):
    """
    Converts a time from one TZ to another.
    The Zone is obtained from the tz() fn
    """
    return time.astimezone(zone)

def apply_appliers(obj, appliers: List[Callable]):
    return reduce(apply_applier, appliers, obj)

def apply_applier(obj, applier: Callable):
    return applier(obj)

def iso8601():
    """
    Generates a callable to convert a time into a ISO8601 Format
    """
    return methodcaller('isoformat')

def epoch():
    """
    Generates a callable to convert a time into a unix epoch timestamp
    """
    return methodcaller('timestamp')

def tz_utc():
    return 'UTC'

def tz(zone_name):
    return pendulum.timezone(zone_name)


def time_now_with_delta_seconds(delta):
    inc = timedelta(seconds=delta)
    return time_now(tz=timezone.utc) + inc

def time_with_delta(time=time_now(tz=timezone.utc), hours=0, minutes=0, seconds=0, direction='inc'):
    delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return time + delta if direction == 'inc' else time - delta


def iso_time_to_date_time(iso_time: str) -> datetime:
    return date_parser(iso_time)

def hours_from_start_from_year(time: datetime) -> int:
    return ((int(time.strftime("%j")) - 1) * 24) + time.hour

def hours_from_start_from_year_to_days_hours(start_time: datetime, hour: int) -> datetime:
    return time_with_delta(start_time, hours=hour)

def now_year_day() -> Tuple[int, int]:
    t = time_now(tz=timezone.utc)
    return (t.year, int(t.strftime("%j")))
