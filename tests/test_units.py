#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.units import Money, Currency


class MoneyTests(unittest.TestCase):

    def test_get_currency(self):
        a = Money('0.1', 'EUR')
        self.assertEquals(str(a), '0.10 Euro')
        b = Money('0.1', 'USD')
        self.assertEquals(str(b), '0.10 US Dollar')
        with self.assertRaises(Exception):
            Money('0.1', 'foobar')
        c = Money((1, 100), 'EUR')
        d = Money(5, 'ESP')
        self.assertEquals(str(c), '0.01 Euro')
        self.assertEquals(repr(c), '0.01 Euro')
        self.assertEquals(str(d), '5.00 Spanish Peseta')
        with self.assertRaises(Exception):
            Money((5, 100, 42), 'EUR')
        with self.assertRaises(Exception):
            Money(0.1, 'EUR')
        with self.assertRaises(Exception):
            Money('0.1', None)

    def test_currency_operations(self):
        a = Money('0.5', 'EUR')
        b = Money('0.1', 'EUR')
        c = Money('0.1', 'USD')
        d = Money('0.5', 'EUR')
        self.assertEquals(a == b, False)
        self.assertEquals(a == 0.5, False)
        self.assertEquals(a == d, True)
        self.assertEquals(a == c, False)
        self.assertEquals(a != b, True)
        self.assertEquals(a != d, False)
        self.assertEquals(a != c, True)
        self.assertEquals(str(a - b), '0.40 Euro')
        with self.assertRaises(Exception):
            a - c
        with self.assertRaises(Exception):
            a - 2
        with self.assertRaises(Exception):
            a - 2.0
        self.assertEquals(str(a + b), '0.60 Euro')
        with self.assertRaises(Exception):
            a + c
        with self.assertRaises(Exception):
            a + 2
        with self.assertRaises(Exception):
            a + 2.0
        self.assertEquals(str(2 * a), '1.00 Euro')
        self.assertEquals(str(a / b), '5')
        with self.assertRaises(Exception):
            a / c
        with self.assertRaises(Exception):
            a * 3.141
        with self.assertRaises(Exception):
            3.141 * a
        with self.assertRaises(Exception):
            a / '0.1'
        self.assertEquals(str(a / 2), '0.25 Euro')

    def test_currency(self):
        eur = Currency(name='Euro',
                       code='EUR',
                       numeric_code=123,
                       symbol='€',
                       exponent=2,
                       entities=['Germany'],
                       withdrawal_date=None,
                       subunits=2)
        usd = Currency(name='US Dollar',
                       code='USD',
                       numeric_code=456,
                       symbol='$',
                       exponent=2,
                       entities=['United States of America'],
                       withdrawal_date=None,
                       subunits=2)
        repr(eur)
        self.assertEquals(eur == usd, False)
        self.assertEquals(eur == 2, False)
        self.assertEquals(eur != usd, True)
        with self.assertRaises(Exception):
            Currency(name=2,
                     code='EUR',
                     numeric_code=123,
                     symbol='€',
                     exponent=2,
                     entities=['Germany'],
                     withdrawal_date=None,
                     subunits=2)
        with self.assertRaises(Exception):
            Currency(name='Euro',
                     code=2,
                     numeric_code=123,
                     symbol='€',
                     exponent=2,
                     entities=['Germany'],
                     withdrawal_date=None,
                     subunits=2)
        with self.assertRaises(Exception):
            Currency(name='Euro',
                     code='EUR',
                     numeric_code=123,
                     symbol='€',
                     exponent='2',
                     entities=['Germany'],
                     withdrawal_date=None,
                     subunits=2)
