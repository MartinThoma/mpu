#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# 3rd party modules
import pandas as pd

# internal modules
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
