#!/usr/bin/env python

"""Handle units - currently only currencies."""


# Core Library
import csv
import fractions
from functools import total_ordering
from typing import Tuple, Union

# Third party
import pkg_resources


class Currency:
    """Currency base class which contains information similar to ISO 4217."""

    def __init__(
        self,
        name,
        code,
        numeric_code,
        symbol,
        exponent,
        entities,
        withdrawal_date,
        subunits,
    ):
        if not isinstance(name, str):
            raise ValueError(
                "A currencies name has to be of type str, but "
                "was: {}".format(type(name))
            )
        if not isinstance(code, str):
            raise ValueError(
                "A currencies code has to be of type str, but "
                "was: {}".format(type(code))
            )
        if not isinstance(exponent, (type(None), int)):
            raise ValueError(
                "A currencies exponent has to be of type None "
                "or int, but was: {}".format(type(code))
            )

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
        return (
            "Currency(name={name}, code={code}, "
            "numeric_code={numeric_code})".format(
                name=self.name, code=self.code, numeric_code=self.numeric_code
            )
        )

    def __json__(self):
        """Return a JSON-serializable object."""
        return {
            "name": self.name,
            "code": self.code,
            "numeric_code": self.numeric_code,
            "symbol": self.symbol,
            "exponent": self.exponent,
            "entities": self.entities,
            "withdrawal_date": self.withdrawal_date,
            "subunits": self.subunits,
            "__python__": "mpu.units:Currency.from_json",
        }

    for_json = __json__

    @classmethod
    def from_json(cls, json):
        """Create a Currency object from a JSON dump."""
        obj = cls(
            name=json["name"],
            code=json["code"],
            numeric_code=json["numeric_code"],
            symbol=json["symbol"],
            exponent=json["exponent"],
            entities=json["entities"],
            withdrawal_date=json["withdrawal_date"],
            subunits=json["subunits"],
        )
        return obj


@total_ordering
class Money:
    """
    Unit of account.

    Parameters
    ----------
    value : Union[str, fractions.Fraction, int, Tuple]
    currency : Currency or str

    Examples
    --------
    >>> rent = Money(500, 'USD')
    >>> '{:.2f,shortcode}'.format(rent)
    'USD 500.00'
    >>> '{:.2f,postshortcode}'.format(rent)
    '500.00 USD'
    >>> '{:.2f,symbol}'.format(rent)
    '$500.00'
    >>> '{:.2f,postsymbol}'.format(rent)
    '500.00$'
    >>> '{:.2f}'.format(rent)
    '500.00 USD'
    """

    def __init__(
        self,
        value: Union[str, fractions.Fraction, int, Tuple],
        currency: Union[str, Currency],
    ):
        # Handle value
        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError(
                    (
                        "value was {}, but only tuples of length 2 "
                        "str, int and decimal are allowed."
                    ).format(value)
                )
            self.value = fractions.Fraction(value[0], value[1])
        elif isinstance(value, float):
            raise ValueError(
                "floats can be ambiguous. Please convert it to "
                "two integers (nominator and denominator) and "
                "pass a tuple to the constructor."
            )
        else:
            self.value = fractions.Fraction(value)  # convert to Decimal

        # Handle currency
        if isinstance(currency, Currency):
            self.currency = currency
        elif isinstance(currency, str):
            self.currency = get_currency(currency)
        elif currency is None:
            self.currency = Currency(
                name="",
                code="",
                numeric_code=None,
                symbol="",
                exponent=None,
                entities=None,
                withdrawal_date=None,
                subunits=None,
            )
        else:
            raise ValueError(
                "currency is of type={}, but should be str or "
                "Currency".format(type(currency))
            )

    def __str__(self):
        exponent = 2
        if self.currency.exponent is not None:
            exponent = self.currency.exponent
        if self.currency.numeric_code is None:
            return "{value:0.{exponent}f}".format(
                exponent=exponent, value=float(self.value)
            )
        else:
            return "{value:0.{exponent}f} {currency}".format(
                exponent=exponent, value=float(self.value), currency=self.currency,
            )

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        if isinstance(other, (int, fractions.Fraction)):
            return Money(self.value * other, self.currency)
        else:
            raise ValueError(
                ("Multiplication with type '{}' is not " "supported").format(
                    type(other)
                )
            )

    def __format__(self, spec):
        if "," not in spec:
            if spec == "":
                exponent = 2
                if self.currency.exponent is not None:
                    exponent = self.currency.exponent
                spec = "0.{exponent:}f".format(exponent=exponent)
            value_formatter = spec
            symbol_formatter = "postshortcode"
        else:
            value_formatter, symbol_formatter = spec.split(",")
        value_str = ("{:" + value_formatter + "}").format(float(self.value))

        if symbol_formatter == "symbol":
            sep = ""
            return self.currency.symbol + sep + value_str
        elif symbol_formatter == "postsymbol":
            sep = ""
            return value_str + sep + self.currency.symbol
        elif symbol_formatter == "shortcode":
            sep = " "
            if self.currency.numeric_code is None:
                sep = ""
            return self.currency.code + sep + value_str
        elif symbol_formatter == "postshortcode":
            sep = " "
            if self.currency.numeric_code is None:
                sep = ""
            return value_str + sep + self.currency.code
        else:
            raise NotImplementedError(
                "The formatter '{}' is not "
                "implemented for the Money class.".format(symbol_formatter)
            )

    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.value + other.value, self.currency)
            else:
                raise ValueError(
                    (
                        "Addition of currency '{}' and '{}' is "
                        "not supported. You need an exchange rate."
                    ).format(self.currency, other.currency)
                )
        else:
            raise ValueError(
                ("Addition with type '{}' is not " "supported").format(type(other))
            )

    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.value - other.value, self.currency)
            else:
                raise ValueError(
                    (
                        "Subtraction of currency '{}' and '{}' "
                        "is not supported. You need an exchange "
                        "rate."
                    ).format(self.currency, other.currency)
                )
        else:
            raise ValueError(
                ("Subtraction with type '{}' is not " "supported").format(type(other))
            )

    def __truediv__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return self.value / other.value
            else:
                raise ValueError(
                    (
                        "Division of currency '{}' and '{}' "
                        "is not supported. You need an exchange "
                        "rate."
                    ).format(self.currency, other.currency)
                )
        elif isinstance(other, (int, fractions.Fraction)):
            return Money(self.value / other, self.currency)
        else:
            raise ValueError(
                ("Division with type '{}' is not " "supported").format(type(other))
            )

    __div__ = __truediv__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            same_currency = self.currency == other.currency
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

    def __neg__(self):
        return Money(-self.value, self.currency)

    def __pos__(self):
        return Money(self.value, self.currency)

    def __float__(self):
        return float(self.value)

    def __json__(self):
        """Return a JSON-serializable object."""
        currency = str(self.currency)
        if self.currency.numeric_code is None:
            currency = None
        return {
            "value": "{}".format(self.value),
            "currency": currency,
            "__python__": "mpu.units:Money.from_json",
        }

    for_json = __json__

    @classmethod
    def from_json(cls, json):
        """Create a Money object from a JSON dump."""
        obj = cls(json["value"], json["currency"])
        return obj


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
    path = "units/currencies.csv"  # always use slash in Python packages
    filepath = pkg_resources.resource_filename("mpu", path)
    with open(filepath) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            is_currency = currency_str in [row[0], row[1], row[2]]
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
                return Currency(
                    name=name,
                    code=code,
                    numeric_code=numeric_code,
                    symbol=symbol,
                    exponent=exponent,
                    entities=[entity],
                    withdrawal_date=withdrawal_date,
                    subunits=subunits,
                )
    raise ValueError("Could not find currency '{}'".format(currency_str))
