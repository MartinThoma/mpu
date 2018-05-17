#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle units - currently only currencies."""

# core modules
import csv
import fractions
import pkg_resources
from functools import total_ordering


@total_ordering
class Money(object):
    """Unit of account."""

    def __init__(self, value, currency):
        # Handle value
        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError(('value was {}, but only tuples of length 2 '
                                  'str, int and decimal are allowed.')
                                 .format(value))
            self.value = fractions.Fraction(value[0], value[1])
        elif isinstance(value, float):
            raise ValueError('floats can be ambiguous. Please convert it to '
                             'two integers (nominator and denominator) and '
                             'pass a tuple to the constructor.')
        else:
            self.value = fractions.Fraction(value)  # convert to Decimal

        # Handle currency
        if isinstance(currency, Currency):
            self.currency = currency
        elif isinstance(currency, str):
            self.currency = get_currency(currency)
        else:
            raise ValueError('currency is of type={}, but should be str or '
                             'Currency')

    def __str__(self):
        exponent = 2
        if self.currency.exponent is not None:
            exponent = self.currency.exponent
        return ('{value:0.{exponent}f} {currency}'
                .format(exponent=exponent,
                        value=float(self.value),
                        currency=self.currency))

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        if isinstance(other, (int, fractions.Fraction)):
            return Money(self.value * other, self.currency)
        else:
            raise ValueError(('Multiplication with type \'{}\' is not '
                              'supported').format(type(other)))

    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.value + other.value, self.currency)
            else:
                raise ValueError(('Addition of currency \'{}\' and \'{}\' is '
                                  'not supported. You need an exchange rate.')
                                 .format(self.currency, other.currency))
        else:
            raise ValueError(('Addition with type \'{}\' is not '
                              'supported').format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.value - other.value, self.currency)
            else:
                raise ValueError(('Subtraction of currency \'{}\' and \'{}\' '
                                  'is not supported. You need an exchange '
                                  'rate.')
                                 .format(self.currency, other.currency))
        else:
            raise ValueError(('Subtraction with type \'{}\' is not '
                              'supported').format(type(other)))

    def __truediv__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return self.value / other.value
            else:
                raise ValueError(('Division of currency \'{}\' and \'{}\' '
                                  'is not supported. You need an exchange '
                                  'rate.')
                                 .format(self.currency, other.currency))
        elif isinstance(other, (int, fractions.Fraction)):
            return Money(self.value / other, self.currency)
        else:
            raise ValueError(('Division with type \'{}\' is not '
                              'supported').format(type(other)))

    __div__ = __truediv__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            same_currency = (self.currency == other.currency)
            return (self.value == other.value) and same_currency
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    __rmul__ = __mul__

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        elif self.currency != other.currency:
            return False
        else:
            return self.value > other.value

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        elif self.currency != other.currency:
            return False
        else:
            return self.value < other.value


def get_currency(currency_str):
    """
    Convert an identifier for a currency into a currency object.

    Parameters
    ----------
    currency_str : str

    Returns
    -------
    currency : Currency
    """
    path = 'units/currencies.csv'  # always use slash in Python packages
    filepath = pkg_resources.resource_filename('mpu', path)
    with open(filepath, 'r') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            is_currency = (row[0] == currency_str or
                           row[1] == currency_str or
                           row[2] == currency_str)
            if is_currency:
                entity = row[0]
                name = row[1]
                code = row[2]
                numeric_code = row[3]
                symbol = row[4]
                if len(row[5]) == 0:
                    exponent = None
                else:
                    exponent = int(row[5])
                if len(row[6]) > 0:
                    withdrawal_date = row[6]
                else:
                    withdrawal_date = None
                subunits = row[7]
                return Currency(name=name,
                                code=code,
                                numeric_code=numeric_code,
                                symbol=symbol,
                                exponent=exponent,
                                entities=[entity],
                                withdrawal_date=withdrawal_date,
                                subunits=subunits)
    raise ValueError('Could not find currency \'{}\''.format(currency_str))


class Currency(object):
    """Currency base class which contains information similar to ISO 4217."""

    def __init__(self,
                 name,
                 code,
                 numeric_code,
                 symbol,
                 exponent,
                 entities,
                 withdrawal_date,
                 subunits):
        if not isinstance(name, str):
            raise ValueError('A currencies name has to be of type str, but '
                             'was: {}'.format(type(name)))
        if not isinstance(code, str):
            raise ValueError('A currencies code has to be of type str, but '
                             'was: {}'.format(type(code)))
        if not isinstance(exponent, (type(None), int)):
            raise ValueError('A currencies exponent has to be of type None '
                             'or int, but was: {}'.format(type(code)))

        self.name = name
        self.code = code
        self.numeric_code = numeric_code
        self.symbol = symbol
        self.exponent = exponent
        self.entities = entities
        self.withdrawal_date = withdrawal_date
        self.subunits = subunits

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.numeric_code == other.numeric_code
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
