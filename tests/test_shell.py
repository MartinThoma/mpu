#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # Python 2.7

# internal modules
from mpu.shell import Codes, text_input, print_table


class ShellTest(unittest.TestCase):

    def test_codes(self):
        s = (Codes.BOLD + Codes.GREEN + 'WORKS!' + Codes.RESET_ALL)
        self.assertIsInstance(s, str)

    def test_text_input(self):
        user_input = ['42']
        with patch('builtins.input', side_effect=user_input):
            self.assertEqual(text_input('Enter something'), '42')

    def test_print_table(self):
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO  # Python 2.7
        import sys

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_table([[1, 2, 3], [41, 0, 1]])
            output = out.getvalue()
            assert output == ' 1  2  3\n41  0  1\n'
        finally:
            sys.stdout = saved_stdout
