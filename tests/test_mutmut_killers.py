# Third party
import pytest

# First party
from mpu.datastructures import Interval
from mpu.units import Money


def test_eq_exception_msg():
    a = Money("0.1", "EUR")
    with pytest.raises(ValueError) as excinfo:
        a == 0.5
    assert "XX" not in str(excinfo)


def test_interval_exception_msg():
    with pytest.raises(RuntimeError) as excinfo:
        Interval(None, 3)
    assert "XX" not in str(excinfo)


def test_interval_left_bigger_right_exception_msg():
    with pytest.raises(RuntimeError) as excinfo:
        Interval(5, 3)
    assert "XX" not in str(excinfo)


def test_interval_invalid_issubset():
    class Impossible:
        def __init__(self):
            self.left = -1
            self.right = float("nan")

        def is_empty(self):
            return False

    interval = Interval(0, 1)
    other = Impossible()
    with pytest.raises(RuntimeError) as excinfo:
        interval.issubset(other)
    assert "XX" not in str(excinfo)
