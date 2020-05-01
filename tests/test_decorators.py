#!/usr/bin/env python

# Core Library
import warnings

# First party
from mpu.decorators import deprecated, timing


def test_timing():
    @timing
    def fib(n):
        if n < 1:
            return n
        else:
            return fib(n - 1) + fib(n - 2)

    fib(2)


def test_deprecated():
    with warnings.catch_warnings(record=True):

        @deprecated
        def fib(n):
            if n < 1:
                return n
            else:
                return fib(n - 1) + fib(n - 2)

        fib(2)
