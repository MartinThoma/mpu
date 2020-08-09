#!/usr/bin/env python

# Core Library
import sys
from io import StringIO

# First party
from mpu.shell import Codes, text_input


def test_codes():
    s = Codes.BOLD + Codes.GREEN + "WORKS!" + Codes.RESET_ALL
    assert isinstance(s, str)


def test_codes_start_with_esc():
    ESC = "\033"  # https://askubuntu.com/q/831971/10425
    codes_obj = Codes()
    codes = [a for a in dir(codes_obj) if not a.startswith("__")]
    for code in codes:
        assert Codes.__dict__[code].startswith(ESC)


def test_text_input():
    sys.stdin = StringIO("foo\nbar")
    text_input("foo")
