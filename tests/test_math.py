#!/usr/bin/env python


# Third party
import pytest

# First party
import mpu.math


def test_factorize_zero():
    with pytest.raises(ValueError):
        mpu.math.factorize(0)


def test_factorize_float():
    with pytest.raises(ValueError):
        mpu.math.factorize(4.0)


def test_argmax():
    assert mpu.math.argmax([1, 2, 3]) == 2
