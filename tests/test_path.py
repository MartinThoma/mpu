#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest
import pkg_resources

# internal modules
from mpu.path import get_all_files


class ImageTests(unittest.TestCase):

    def test_get_meta(self):
        path = '../tests/files'
        root = pkg_resources.resource_filename('mpu', path)
        meta = get_all_files(root)
        self.assertEqual(len(meta), 5)
