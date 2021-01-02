#!/usr/bin/env python


# Core Library
from datetime import datetime

# Third party
import pytest
import pytz

# First party
import mpu.datetime


def test_add_hour():
    tz = pytz.timezone("Europe/Berlin")
    out = mpu.datetime.add_time(
        datetime(1918, 4, 15, 0, 0, tzinfo=pytz.utc).astimezone(tz), hours=1
    ).isoformat()
    assert out == "1918-04-15T03:00:00+02:00"


def test_add_day():
    tz = pytz.timezone("Europe/Berlin")
    out = mpu.datetime.add_time(
        datetime(1918, 4, 15, 0, 0, tzinfo=pytz.utc).astimezone(tz),
        days=1,
    ).isoformat()
    assert out == "1918-04-16T02:00:00+02:00"


def test_add_time_neutral():
    """Call add_time without any specified time to add."""
    tz = pytz.timezone("Europe/Berlin")
    out = mpu.datetime.add_time(
        datetime(1918, 4, 15, 0, 0, tzinfo=pytz.utc).astimezone(tz)
    ).isoformat()
    assert out == "1918-04-15T01:00:00+01:00"


def test_add_time_all():
    """Call add_time without any specified time to add."""
    tz = pytz.timezone("Europe/Berlin")
    out = mpu.datetime.add_time(
        datetime(1918, 4, 15, 0, 0, tzinfo=pytz.utc).astimezone(tz),
        seconds=1,
        minutes=2,
        hours=3,
    ).isoformat()
    assert out == "1918-04-15T05:02:01+02:00"


def test_generate_fail():
    with pytest.raises(ValueError):
        mpu.datetime.generate(datetime(2018, 1, 1), datetime(2018, 1, 1))


def test_generate():
    start = datetime(2018, 1, 1)
    end = datetime(2018, 2, 1)
    generated = mpu.datetime.generate(start, end)
    assert start <= generated <= end
