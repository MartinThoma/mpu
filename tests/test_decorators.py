#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest
import warnings

# internal modules
from mpu.decorators import timing, deprecated


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
