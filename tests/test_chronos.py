import pytest
from datetime import datetime
import time_machine

from metis_fn import chronos


def it_returns_time_now_in_iso_utc():
    time_now_utc = chronos.time_now(tz=chronos.tz_utc())
    assert (time_now_utc.tzname()) == 'UTC'


def it_returns_time_in_iso8601_format():
    time_now_utc_iso = chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.iso8601()])

    assert isinstance(time_now_utc_iso, str)
    assert '+00:00' in time_now_utc_iso


def it_returns_time_as_epoch():
    time_epoch = chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])

    assert isinstance(time_epoch, float)


@time_machine.travel(chronos.try_parse_iso8601_time("2021-10-16T09:00:00Z").value)
def it_converts_time_from_utc_to_alternate_tz():
    pass
    # utc_now = chronos.time_now(tz=chronos.tz_utc())
    # sydney_time = chronos.tz_convert(utc_now, chronos.tz('Australia/Sydney'))
    #
    # breakpoint()
    # expected_time = chronos.tz('Australia/Sydney').localize(datetime(2021, 10, 16, 20, 0), is_dst=True)
    #
    # assert sydney_time == expected_time


@time_machine.travel(chronos.try_parse_iso8601_time("2021-10-16T09:00:00Z").value)
def it_converts_time_from_tz_to_utc():
    sydney_time = chronos.time_now(tz=chronos.tz('Australia/Sydney'))

    utc_time = chronos.tz_convert(sydney_time, chronos.tz('UTC'))

    assert sydney_time.hour == 20
    assert utc_time.hour == 9


@time_machine.travel(chronos.try_parse_iso8601_time("2021-08-02T09:05:00Z").value)
def it_generates_now_year_and_day():
    year, day = chronos.now_year_day()

    assert year == 2021
    assert day == 214


@time_machine.travel(chronos.try_parse_iso8601_time("2021-10-02T09:05:00Z").value)
def it_moves_deltas():
    time = chronos.try_parse_iso8601_time("2021-10-02T09:05:00Z").value

    delta_t_forward = chronos.time_with_delta(time, hours=12, direction='inc')

    assert (delta_t_forward.hour) == 21

    delta_t_back = chronos.time_with_delta(time, hours=12, direction='dec')

    assert (delta_t_back.hour) == 21
    assert (delta_t_back.day) == 1
