#!/usr/bin/env python

# Core Library
import sys
from io import StringIO

# First party
from mpu.shell import Codes, text_input


def test_codes():
    s = Codes.BOLD + Codes.GREEN + "WORKS!" + Codes.RESET_ALL
    assert isinstance(s, str)


def test_text_input():
    sys.stdin = StringIO("foo\nbar")
    text_input("foo")
