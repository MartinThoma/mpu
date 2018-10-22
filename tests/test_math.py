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

    def test_factorize(self):
        assert mpu.math.factorize(-17) == [-1, 17]
        assert mpu.math.factorize(8) == [2, 2, 2]
        assert mpu.math.factorize(1) == [1]

    def test_argmax(self):
        self.assertEqual(mpu.math.argmax([1, 2, 3]), 2)
