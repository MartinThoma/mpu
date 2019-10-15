#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Core Library
import unittest

# First party
import mpu.math


class MathTest(unittest.TestCase):

    def test_factorize_zero(self):
        with self.assertRaises(ValueError):
            mpu.math.factorize(0)

    def test_factorize_float(self):
        with self.assertRaises(ValueError):
            mpu.math.factorize(4.0)

    def test_argmax(self):
        self.assertEqual(mpu.math.argmax([1, 2, 3]), 2)
