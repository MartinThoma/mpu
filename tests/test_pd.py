#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.pd import example_df


class DatastructuresTest(unittest.TestCase):

    def test_example_df(self):
        example_df()
