#!/usr/bin/env python
# -*- coding: utf-8 -*-

# First party
from mpu.shell import Codes, text_input


def test_codes():
    s = Codes.BOLD + Codes.GREEN + "WORKS!" + Codes.RESET_ALL
    assert isinstance(s, str)


def test_text_input():
    try:
        from io import StringIO
    except ImportError:
        from StringIO import StringIO
    import sys

    sys.stdin = StringIO(u"foo\nbar")
    text_input("foo")
