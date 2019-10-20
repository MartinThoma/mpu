#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Third party
import pytest

# First party
import mpu.string


def test_str2bool():
    with pytest.raises(ValueError):
        mpu.string.str2bool("foobar")


def test_is_iban_not():
    assert mpu.string.is_iban("DE12") is False
    assert mpu.string.is_iban("") is False
    assert mpu.string.is_iban("ZZaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") is False
    assert mpu.string.is_iban("DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") is False


def test_is_iban():
    iban = "FR14 2004 1010 0505 0001 3M02 606"
    assert mpu.string.is_iban(iban)


def test_is_none_not():
    with pytest.raises(ValueError):
        mpu.string.is_none("foobar")
