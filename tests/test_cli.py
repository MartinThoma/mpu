#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# core modules
import unittest

# internal modules
import mpu._cli


class CliTest(unittest.TestCase):

    def test_get_parser(self):
        mpu._cli.get_parser()
