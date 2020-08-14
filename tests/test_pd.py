#!/usr/bin/env python

# Core Library
import datetime

# Third party
import pandas as pd

# First party
import mpu.pd


def test_example_df():
    df = mpu.pd.example_df()
    assert list(df.columns) == ["country", "population", "population_time", "EUR"]
    assert list(df["country"]) == [
        "Germany",
        "France",
        "Indonesia",
        "Ireland",
        "Spain",
        "Vatican",
    ]
    assert list(df["population"])[:5] == [
        82521653.0,
        66991000.0,
        255461700.0,
        4761865.0,
        46549045.0,
    ]
    assert df["population_time"].equals(
        pd.Series(
            [
                datetime.datetime(2016, 12, 1),
                datetime.datetime(2017, 1, 1),
                datetime.datetime(2017, 1, 1),
                None,  # Ireland
                datetime.datetime(2017, 6, 1),  # Spain
                None,
            ]
        )
    )
    assert list(df["EUR"]) == [True, True, False, True, True, True]


def test_describe():
    mpu.pd.describe(mpu.pd.example_df())


def test_describe_int():
    column_info = {"int": ["numbers"]}
    df = pd.DataFrame({"numbers": [1, 2, 3, 100, 500]})
    mpu.pd._describe_int(df, column_info)
    mpu.pd.describe(df, column_info)


def test_get_column_info_suspicious_categorical():
    df = pd.DataFrame({"numbers": [1, 2, 3, 100, 500]})
    mpu.pd._get_column_info(df, [])


def test_get_column_info_nonsuspicious_categorical():
    df = pd.DataFrame({"numbers": [i for i in range(200)]})
    mpu.pd._get_column_info(df, [])


def test_get_column_info_no_values():
    df = pd.DataFrame({"numbers": []})
    mpu.pd._get_column_info(df, [])


def test_get_column_info_mixed_column():
    df = pd.DataFrame({"numbers": [1, 2.3, None, "Foobar", (5, 10)]})
    info = mpu.pd._get_column_info(df, [])

    assert set(info[1]["numbers"]["value_list"]) == {(5, 10), 2.3, "Foobar", 1}
    info[1]["numbers"]["value_list"] = None

    expected_column_info = {
        "category": [],
        "float": [],
        "int": [],
        "other": ["numbers"],
        "time": [],
    }
    expected_column_meta = {
        "numbers": {"top_count_val": 1, "value_list": None, "value_count": 4}
    }
    expected = (expected_column_info, expected_column_meta)
    assert info == expected


def test_get_column_info_column_unknown_dtype():
    df = pd.DataFrame({"numbers": [datetime.timedelta(days=3)]})
    info = mpu.pd._get_column_info(df, [])

    assert set(info[1]["numbers"]["value_list"]) == {datetime.timedelta(days=3)}
    info[1]["numbers"]["value_list"] = None

    expected_column_info = {
        "category": [],
        "float": [],
        "int": [],
        "other": [],
        "time": [],
    }
    expected_column_meta = {
        "numbers": {"top_count_val": 1, "value_list": None, "value_count": 1}
    }
    expected = (expected_column_info, expected_column_meta)
    assert info == expected


def test_countries_global():
    assert len(mpu.pd.countries) == 248
