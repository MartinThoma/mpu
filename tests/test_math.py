#!/usr/bin/env python


# Third party
import hypothesis.strategies as s
import pytest
from hypothesis import given

# First party
import mpu.math


def test_factorize_zero():
    with pytest.raises(ValueError):
        mpu.math.factorize(0)


@given(s.floats())
def test_factorize_float(a_float):
    with pytest.raises(ValueError):
        mpu.math.factorize(a_float)


@given(s.integers(min_value=-(10 ** 6), max_value=10 ** 6))
def test_factorize(an_integer):
    if an_integer == 0:
        # This is tested in `test_factorize_zero` and should throw an exception
        return
    factors = mpu.math.factorize(an_integer)
    product = 1
    for factor in factors:
        product *= factor
    assert product == an_integer


def test_argmax():
    assert mpu.math.argmax([1, 2, 3]) == 2


def test_gcd_fail():
    with pytest.raises(ValueError):
        mpu.math.gcd(0, 7)
