#!/usr/bin/env python

"""Pandas utility functions."""


# Core Library
import datetime as dt
import logging
from typing import Any, Dict, List, Tuple

# Third party
import pandas as pd
import pkg_resources

# First party
import mpu.shell

countries_file = pkg_resources.resource_filename("mpu", "data/countries.csv")
countries = pd.read_csv(countries_file)
logger = logging.getLogger("mpu")


def example_df():
    """Create an example dataframe."""
    country_names = ["Germany", "France", "Indonesia", "Ireland", "Spain", "Vatican"]
    population = [82521653, 66991000, 255461700, 4761865, 46549045, None]
    population_time = [
        dt.datetime(2016, 12, 1),
        dt.datetime(2017, 1, 1),
        dt.datetime(2017, 1, 1),
        None,  # Ireland
        dt.datetime(2017, 6, 1),  # Spain
        None,
    ]
    euro = [True, True, False, True, True, True]
    df = pd.DataFrame(
        {
            "country": country_names,
            "population": population,
            "population_time": population_time,
            "EUR": euro,
        }
    )
    df = df[["country", "population", "population_time", "EUR"]]
    return df


def describe(df, dtype=None):
    """
    Print a description of a Pandas dataframe.

    Parameters
    ----------
    df : Pandas.DataFrame
    dtype : dict
        Maps column names to types
    """
    if dtype is None:
        dtype = {}
    print("Number of datapoints: {datapoints}".format(datapoints=len(df)))
    column_info, column_info_meta = _get_column_info(df, dtype)

    if len(column_info["int"]) > 0:
        _describe_int(df, column_info)

    if len(column_info["float"]) > 0:
        _describe_float(df, column_info)

    if len(column_info["category"]) > 0:
        _describe_category(df, column_info, column_info_meta)

    if len(column_info["time"]) > 0:
        _describe_time(df, column_info, column_info_meta)

    if len(column_info["other"]) > 0:
        _describe_other(df, column_info, column_info_meta)

    column_types = {}
    for column_type, columns in column_info.items():
        for column_name in columns:
            if column_type == "other":
                column_type = "str"
            column_types[column_name] = column_type
    return column_types


def _get_column_info(df: pd.DataFrame, dtype: Dict[str, str]) -> Tuple[Dict, Dict]:
    column_info: Dict[str, List[str]] = {
        "int": [],
        "float": [],
        "category": [],
        "other": [],
        "time": [],
    }
    float_types = ["float64"]
    integer_types = ["int64", "uint8"]
    time_types = ["datetime64[ns]"]
    other_types = ["object", "category"]
    column_info_meta: Dict[str, Dict[str, Any]] = {}
    for column_name in df:
        column_info_meta[column_name] = {}
        counter_obj = df[column_name].value_counts()
        value_list = counter_obj.keys().tolist()
        value_count = len(value_list)
        is_suspicious_cat = (
            value_count <= 50
            and str(df[column_name].dtype) != "category"
            and column_name not in dtype
        )
        if is_suspicious_cat:
            logger.warning(
                "Column '{}' has only {} different values ({}). "
                "You might want to make it a 'category'".format(
                    column_name, value_count, value_list
                )
            )
        if len(value_list) > 0:
            top_count_val = counter_obj.tolist()[0]
        else:
            top_count_val = None
        column_info_meta[column_name]["top_count_val"] = top_count_val
        column_info_meta[column_name]["value_list"] = value_list
        column_info_meta[column_name]["value_count"] = value_count
        is_int_type = (
            df[column_name].dtype in integer_types
            or column_name in dtype
            and dtype[column_name] in integer_types
        )
        is_float_type = (
            df[column_name].dtype in float_types
            or column_name in dtype
            and dtype[column_name] in float_types
        )
        is_cat_type = (
            str(df[column_name].dtype) in ["category", "bool"]
            or column_name in dtype
            and dtype[column_name] in ["category", "bool"]
        )
        is_time_type = str(df[column_name].dtype) in time_types
        is_other_type = (
            str(df[column_name].dtype) in other_types
            or column_name in dtype
            and dtype[column_name] in other_types
        )
        if is_int_type:
            column_info["int"].append(column_name)
        elif is_float_type:
            column_info["float"].append(column_name)
        elif is_cat_type:
            column_info["category"].append(column_name)
        elif is_other_type:
            column_info["other"].append(column_name)
        elif is_time_type:
            column_info["time"].append(column_name)
        else:
            logger.warning(
                "mpu.pd.describe does not know type '{}'".format(df[column_name].dtype)
            )
    return column_info, column_info_meta


def _describe_int(df, column_info):
    print("\n## Integer Columns")
    table = [
        ["Column name", "Non-nan", "mean", "std", "min", "25%", "50%", "75%", "max"]
    ]
    for column_name in column_info["int"]:
        row = []
        row.append(column_name)
        row.append(sum(df[column_name].notnull()))
        row.append(df[column_name].mean())
        row.append(df[column_name].std())
        row.append(df[column_name].min())
        row.append(df[column_name].quantile(0.25))
        row.append(df[column_name].quantile(0.50))
        row.append(df[column_name].quantile(0.75))
        row.append(max(df[column_name]))
        table.append(row)
    mpu.shell.print_table(table)


def _describe_float(df, column_info):
    print("\n## Float Columns")
    table = [
        ["Column name", "Non-nan", "mean", "std", "min", "25%", "50%", "75%", "max"]
    ]
    for column_name in column_info["float"]:
        row = []
        row.append(column_name)
        row.append(sum(df[column_name].notnull()))
        row.append("{:0.2f}".format(df[column_name].mean()))
        row.append("{:0.2f}".format(df[column_name].std()))
        row.append("{:0.2f}".format(df[column_name].min()))
        row.append("{:0.2f}".format(df[column_name].quantile(0.25)))
        row.append("{:0.2f}".format(df[column_name].quantile(0.50)))
        row.append("{:0.2f}".format(df[column_name].quantile(0.75)))
        row.append("{:0.2f}".format(max(df[column_name])))
        table.append(row)
    mpu.shell.print_table(table)


def _describe_category(df, column_info, column_info_meta):
    print("\n## Category Columns")
    table = [["Column name", "Non-nan", "unique", "top el", "top (count)", "rest"]]
    for column_name in column_info["category"]:
        row = []
        row.append(column_name)
        row.append(sum(df[column_name].notnull()))
        row.append(len(df[column_name].unique()))
        row.append(column_info_meta[column_name]["value_list"][0])
        row.append(column_info_meta[column_name]["top_count_val"])
        rest = str(column_info_meta[column_name]["value_list"][1:])[:40]
        row.append(rest)
        table.append(row)
    mpu.shell.print_table(table)


def _describe_time(df, column_info, column_info_meta):
    print("\n## Time Columns")
    table = [
        ["Column name", "Non-nan", "unique", "top el", "top (count)", "min", "max"]
    ]
    for column_name in column_info["time"]:
        row = []
        row.append(column_name)
        row.append(sum(df[column_name].notnull()))
        row.append(len(df[column_name].unique()))
        row.append(column_info_meta[column_name]["value_list"][0])
        row.append(column_info_meta[column_name]["top_count_val"])
        row.append(df[column_name].min())
        row.append(df[column_name].max())
        table.append(row)
    mpu.shell.print_table(table)


def _describe_other(df, column_info, column_info_meta):
    print("\n## Other Columns")
    table = [["Column name", "Non-nan", "unique", "top", "(count)", "rest"]]
    for column_name in column_info["other"]:
        row = []
        row.append(column_name)
        row.append(sum(df[column_name].notnull()))
        row.append(len(df[column_name].unique()))
        row.append(column_info_meta[column_name]["value_list"][0])
        row.append(column_info_meta[column_name]["top_count_val"])
        rest = str(column_info_meta[column_name]["value_list"][1:])[:40]
        row.append(rest)
        table.append(row)
    mpu.shell.print_table(table)
