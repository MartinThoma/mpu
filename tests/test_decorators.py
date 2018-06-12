#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.decorators import timing


class DecoratorTests(unittest.TestCase):
    def test_timing(self):
        @timing
        def fib(n):
            if n < 1:
                return n
            else:
                return fib(n - 1) + fib(n - 2)

        fib(2)
