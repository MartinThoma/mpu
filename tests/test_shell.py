#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.shell import Codes


class ShellTest(unittest.TestCase):

    def test_codes(self):
        s = (Codes.BOLD + Codes.GREEN + 'WORKS!' + Codes.RESET_ALL)
        self.assertIsInstance(s, str)
