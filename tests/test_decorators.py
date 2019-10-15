#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library
import unittest
import warnings

# First party
from mpu.decorators import deprecated, timing


class DecoratorTests(unittest.TestCase):
    def test_timing(self):
        @timing
        def fib(n):
            if n < 1:
                return n
            else:
                return fib(n - 1) + fib(n - 2)

        fib(2)

    def test_deprecated(self):
        with warnings.catch_warnings(record=True):
            @deprecated
            def fib(n):
                if n < 1:
                    return n
                else:
                    return fib(n - 1) + fib(n - 2)

            fib(2)
