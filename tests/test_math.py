#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# core modules
import unittest

# internal modules
import mpu.math


class MathTest(unittest.TestCase):

    def test_factorize_zero(self):
        with self.assertRaises(ValueError):
            mpu.math.factorize(0)

    def test_factorize_float(self):
        with self.assertRaises(ValueError):
            mpu.math.factorize(4.0)

    def test_argmax(self):
        self.assertEquals(mpu.math.argmax([1, 2, 3]), 2)
