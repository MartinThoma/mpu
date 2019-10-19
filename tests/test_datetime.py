#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

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


def test_generate_fail():
    with pytest.raises(ValueError):
        mpu.datetime.generate(datetime(2018, 1, 1), datetime(2018, 1, 1))
