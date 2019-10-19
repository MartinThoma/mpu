#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library
import sys
import traceback

import pytest

# First party
from mpu import (
    Location,
    clip,
    exception_logging,
    haversine_distance,
    is_in_intervall,
    parallel_for,
)


def test_clip():
    assert clip(42) == 42
    assert clip(42, 0, 100) == 42
    assert clip(42, 0, 42.0) == 42


def test_parallel_for():
    import time

    def looping_function(payload):
        i, j = payload
        time.sleep(1)
        return i + j

    parameters = list((i, i + 1) for i in range(50))
    out = parallel_for(looping_function, parameters)
    assert out == [2 * i + 1 for i in range(50)]


def test_haversine():
    with pytest.raises(ValueError):
        haversine_distance((-200, 0), (0, 0))
    with pytest.raises(ValueError):
        haversine_distance((0, -200), (0, 0))
    with pytest.raises(ValueError):
        haversine_distance((0, 0), (-200, 0))
    with pytest.raises(ValueError):
        haversine_distance((0, 0), (0, -200))


def test_is_in_intervall_raises():
    with pytest.raises(ValueError):
        is_in_intervall(10, 20, 100)


def test_is_in_intervall_ok():
    is_in_intervall(10, 10, 100)


def test_exception_logging():
    def raise_exception():
        try:
            raise Exception
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)
        return tb

    exception_logging(exctype="ValueError", value=None, tb=raise_exception())


def test_location_class():
    munich = Location(48.137222222222, 11.575555555556)
    berlin = Location(52.518611111111, 13.408333333333)
    assert abs(munich.distance(berlin) - 506.7) < 10
