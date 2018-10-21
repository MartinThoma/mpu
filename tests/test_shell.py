#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.shell import Codes, text_input


class ShellTest(unittest.TestCase):

    def test_codes(self):
        s = (Codes.BOLD + Codes.GREEN + 'WORKS!' + Codes.RESET_ALL)
        self.assertIsInstance(s, str)

    def test_text_input(self):
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
        import sys
        sys.stdin = StringIO("foo\nbar")
        text_input('foo')
