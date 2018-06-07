#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.string import str2bool


class StringTests(unittest.TestCase):

    def test_str2bool(self):
        with self.assertRaises(ValueError):
            str2bool('foobar')
