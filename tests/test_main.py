#!/usr/bin/env python

# Core Library
import sys
import traceback

# Third party
import pytest

# First party
from mpu import (
    Location,
    clip,
    consistent_shuffle,
    exception_logging,
    haversine_distance,
    is_in_intervall,
    parallel_for,
)


def test_clip():
    assert clip(42) == 42
    assert clip(42, 0, 100) == 42
    assert clip(42, 0, 42.0) == 42
    assert clip(42, None, 100) == 42
    assert clip(42, 0, None) == 42
    assert clip(-42, 0, None) == 0
    assert clip(420, None, 100) == 100


def test_parallel_for():
    import time

    def looping_function(payload):
        i, j = payload
        time.sleep(1)
        return i + j

    parameters = [(i, i + 1) for i in range(50)]
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
    assert "google.com" in munich.get_google_maps_link()
    assert munich.get_google_maps_link().startswith("http")


def test_location_value_range():
    with pytest.raises(ValueError):
        Location(90.000000001, 42)
    with pytest.raises(ValueError):
        Location(-90.000000001, 42)
    Location(90.0, 42)
    Location(-90.0, 42)
    with pytest.raises(ValueError):
        Location(42, 180.000000001)
    with pytest.raises(ValueError):
        Location(42, -180.000000001)
    Location(42, 180.0)
    Location(42, -180.0)


def test_consistent_shuffle_singe():
    input_list = [1, 2, 3]
    result = consistent_shuffle(input_list)
    assert set(input_list) == set(result[0])
