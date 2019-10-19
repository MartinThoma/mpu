#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Third party
import pkg_resources

# First party
from mpu.path import get_all_files, get_from_package


def test_get_meta():
    path = "files"
    root = pkg_resources.resource_filename(__name__, path)
    meta = get_all_files(root)
    assert len(meta) == 5


def test_get_from_package():
    get_from_package("mpu", "data/iban.csv")
