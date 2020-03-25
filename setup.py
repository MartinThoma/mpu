#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mpu: Martins Python Utilities."""

# Third party
from setuptools import setup

requires_datetime = ["pytz"]
requires_image = ["Pillow"]
requires_io = ["pytz", "tzlocal"]
requires_aws = ["boto3"]
requires_tests = [
    "pytest",
    "pytest-cov",
    "pytest-mccabe",
    "pytest-flake8",
    "simplejson",
]
requires_all = (
    ["pandas", "python-magic"]
    + requires_datetime
    + requires_image
    + requires_io
    + requires_aws
    + requires_tests
)

setup(
    package_data={"mpu": ["units/currencies.csv", "data/*", "package/templates/*"]},
    extras_require={
        "all": requires_all,
        "aws": requires_aws,
        "datetime": requires_datetime,
        "image": requires_image,
        "io": requires_io,
        "tests": requires_tests,
    },
    tests_require=requires_tests,
)
