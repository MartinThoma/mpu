#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library
import unittest

# Third party
import pkg_resources

# First party
from mpu.path import get_all_files, get_from_package


class ImageTests(unittest.TestCase):

    def test_get_meta(self):
        path = 'files'
        root = pkg_resources.resource_filename(__name__, path)
        meta = get_all_files(root)
        self.assertEqual(len(meta), 5)

    def test_get_from_package(self):
        get_from_package('mpu', 'data/iban.csv')
