#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# core modules
import unittest

# internal modules
from mpu.shell import Codes, print_table


class ShellTest(unittest.TestCase):

    def test_codes(self):
        s = (Codes.BOLD + Codes.GREEN + 'WORKS!' + Codes.RESET_ALL)
        self.assertIsInstance(s, str)


def test_print_table(capsys):
    print_table([[1, 2, 3], [41, 0, 1]])
    output, err = capsys.readouterr()
    assert output == ' 1  2  3\n41  0  1\n'
