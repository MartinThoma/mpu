#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest
import pkg_resources

# internal modules
from mpu.image import get_meta


class ImageTests(unittest.TestCase):

    def test_get_meta(self):
        path = '../tests/files/example.png'
        source = pkg_resources.resource_filename('mpu', path)
        meta = get_meta(source)
        meta['file'] = None
        self.assertDictEqual(meta, {'width': 252, 'height': 167,
                                    'channels': 4,
                                    'file': None})
