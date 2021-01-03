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


def test_describe(capsys):
    mpu.pd.describe(mpu.pd.example_df())
    captured = capsys.readouterr()
    assert (
        captured.out
        == """Number of datapoints: 6

## Float Columns
Column name  Non-nan         mean          std         min          25%          50%          75%           max
 population        5  91257052.60  96317882.77  4761865.00  46549045.00  66991000.00  82521653.00  255461700.00

## Category Columns
Column name  Non-nan  unique  top el  top (count)    rest
        EUR        6       2   False            5  [True]

## Time Columns
    Column name  Non-nan  unique               top el  top (count)                  min                  max
population_time        4       4  2016-12-01 00:00:00            2  2016-12-01 00:00:00  2017-06-01 00:00:00

## Other Columns
Column name  Non-nan  unique     top  (count)                                      rest
    country        6       6  France        1  ['Germany', 'Indonesia', 'Ireland', 'Spa
"""
    )


def test_describe_int(capsys):
    column_info = {"int": ["numbers"]}
    df = pd.DataFrame({"numbers": [1, 2, 3, 100, 500]})
    mpu.pd._describe_int(df, column_info)
    mpu.pd.describe(df, column_info)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """
## Integer Columns
Column name  Non-nan   mean                 std  min  25%  50%    75%  max
    numbers        5  121.2  215.96689561134133    1  2.0  3.0  100.0  500
Number of datapoints: 5

## Integer Columns
Column name  Non-nan   mean                 std  min  25%  50%    75%  max
    numbers        5  121.2  215.96689561134133    1  2.0  3.0  100.0  500
"""
    )


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
