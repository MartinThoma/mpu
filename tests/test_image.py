#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library
import unittest

# Third party
import pkg_resources

# First party
from mpu.image import get_meta


class ImageTests(unittest.TestCase):

    def test_get_meta(self):
        path = 'files/example.png'
        source = pkg_resources.resource_filename(__name__, path)
        meta = get_meta(source)
        meta['file'] = None
        self.assertDictEqual(meta, {'width': 252, 'height': 167,
                                    'channels': 4,
                                    'file': None})
