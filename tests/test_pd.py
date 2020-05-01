#!/usr/bin/env python

# Third party
import pandas as pd

# First party
import mpu.pd


def test_example_df():
    mpu.pd.example_df()


def test_describe():
    mpu.pd.describe(mpu.pd.example_df())


def test_describe_int():
    column_info = {"int": ["numbers"]}
    df = pd.DataFrame({"numbers": [1, 2, 3, 100, 500]})
    mpu.pd._describe_int(df, column_info)
    mpu.pd.describe(df, column_info)
