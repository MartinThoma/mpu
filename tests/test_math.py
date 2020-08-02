#!/usr/bin/env python


# Core Library
import itertools

# Third party
import hypothesis.strategies as st
import pytest
from hypothesis import given

# First party
import mpu.math


def test_factorize_zero():
    with pytest.raises(ValueError):
        mpu.math.factorize(0)


@given(st.floats())
def test_factorize_float(a_float):
    with pytest.raises(ValueError):
        mpu.math.factorize(a_float)


def test_factorize_at_border():
    assert mpu.math.factorize(991 ** 2) == [991, 991]


@given(st.integers(min_value=-(10 ** 6), max_value=10 ** 6))
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


@given(st.lists(st.integers(), min_size=1))
def test_argmax_property(integer_list):
    argmax = mpu.math.argmax(integer_list)
    max_value = integer_list[argmax]
    for el in integer_list:
        assert el <= max_value


def test_gcd_fail():
    with pytest.raises(ValueError):
        mpu.math.gcd(0, 7)


@given(st.integers(), st.integers())
def test_gcd_property(a, b):
    if a == 0 or b == 0:
        with pytest.raises(ValueError):
            mpu.math.gcd(a, b)
    else:
        gcd = mpu.math.gcd(a, b)
        assert a % gcd == 0
        assert b % gcd == 0


def test_generate_primes():
    first_primes = list(itertools.islice(mpu.math.generate_primes(), 10))
    assert first_primes == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
