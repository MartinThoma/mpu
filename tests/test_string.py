#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
import mpu.string


class StringTests(unittest.TestCase):

    def test_str2bool(self):
        with self.assertRaises(ValueError):
            mpu.string.str2bool('foobar')

    def test_is_iban_not(self):
        self.assertFalse(mpu.string.is_iban('DE12'))
        self.assertFalse(mpu.string.is_iban(''))
        self.assertFalse(mpu.string.is_iban('ZZaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))
        self.assertFalse(mpu.string.is_iban('DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))

    def test_is_iban(self):
        iban = 'FR14 2004 1010 0505 0001 3M02 606'
        self.assertTrue(mpu.string.is_iban(iban))

    def test_is_none_not(self):
        with self.assertRaises(ValueError):
            mpu.string.is_none('foobar')
