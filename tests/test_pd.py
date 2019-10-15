#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library
import unittest

# Third party
import pandas as pd

# First party
import mpu.pd


class DatastructuresTest(unittest.TestCase):

    def test_example_df(self):
        mpu.pd.example_df()

    def test_describe(self):
        mpu.pd.describe(mpu.pd.example_df())

    def test_describe_int(self):
        column_info = {'int': ['numbers']}
        df = pd.DataFrame({'numbers': [1, 2, 3, 100, 500]})
        mpu.pd._describe_int(df, column_info)
        mpu.pd.describe(df, column_info)
