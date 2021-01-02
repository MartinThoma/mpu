#!/usr/bin/env python

"""Test the mpu.units module."""

# Third party
import pytest
import simplejson  # has for_json

# First party
from mpu.units import Currency, Money, get_currency


def test_get_currency():
    a = Money("0.1", "EUR")
    assert str(a) == "0.10 Euro"
    b = Money("0.1", "USD")
    assert str(b) == "0.10 US Dollar"
    with pytest.raises(ValueError):
        Money("0.1", "foobar")
    c = Money((1, 100), "EUR")
    d = Money(5, "ESP")
    assert str(c) == "0.01 Euro"
    assert repr(c) == "0.01 Euro"
    assert str(d) == "5.00 Spanish Peseta"
    with pytest.raises(ValueError):
        Money((5, 100, 42), "EUR")
    with pytest.raises(ValueError):
        Money(0.1, "EUR")
    non_currency = Money("0.1", None)
    assert str(non_currency) == "0.10"
    with pytest.raises(ValueError):
        Money(1, a)


def test_currency_for_json():
    usd = get_currency("USD")
    dump = simplejson.dumps(usd, for_json=True)
    dict_ = simplejson.loads(dump)
    undump = Currency.from_json(dict_)
    assert usd == undump


def test_money_json_magic():
    usd = Money("0.1", "USD")
    usd_dict = usd.__json__()
    dump = simplejson.dumps(usd_dict)
    dict_ = simplejson.loads(dump)
    undump = Money.from_json(dict_)
    assert usd == undump


def test_money_json_magic_none():
    usd = Money("0.1", None)
    usd_dict = usd.__json__()
    dump = simplejson.dumps(usd_dict)
    dict_ = simplejson.loads(dump)
    undump = Money.from_json(dict_)
    assert usd == undump


def test_money_conversion_float():
    """Test if one can convert Money instances to float."""
    a = Money("1337.00", None)
    assert float(a) == 1337.0
    b = Money("42.00", "USD")
    assert float(b) == 42.0


def test_money_floatingpoint_issue1():
    """The test is the reason why one should not use float for money."""
    a = Money("10.00", None)
    b = Money("1.2", None)
    assert str(a + b - a) == str(b)


def test_money_floatingpoint_issue2():
    """The test is the reason why one should not use float for money."""
    a = Money("10.00", None)
    b = Money("1.2", None)
    assert str((a + b - a) * 10 ** 14 - b * 10 ** 14) == "0.00"


def test_currency_operations():
    a = Money("0.5", "EUR")
    aneg = Money("-0.5", "EUR")
    b = Money("0.1", "EUR")
    c = Money("0.1", "USD")
    d = Money("0.5", "EUR")
    assert (a == b) is False
    with pytest.raises(ValueError):
        a == 0.5
    assert a == d
    with pytest.raises(ValueError):
        a == c
    assert a != b
    assert (a != d) is False
    with pytest.raises(ValueError):
        a != c
    assert str(a - b) == "0.40 Euro"
    assert -a == aneg
    assert +a == a
    with pytest.raises(ValueError):
        a - c
    with pytest.raises(ValueError):
        a - 2
    with pytest.raises(ValueError):
        a - 2.0
    assert str(a + b) == "0.60 Euro"
    with pytest.raises(ValueError):
        a + c
    with pytest.raises(ValueError):
        a + 2
    with pytest.raises(ValueError):
        a + 2.0
    assert str(2 * a) == "1.00 Euro"
    assert str(a / b) == "5"
    with pytest.raises(ValueError):
        a / c
    with pytest.raises(ValueError):
        a * 3.141
    with pytest.raises(ValueError):
        3.141 * a
    with pytest.raises(ValueError):
        a / "0.1"
    assert str(a / 2) == "0.25 Euro"


def test_currency_comperators():
    a = Money("0.5", "EUR")
    b = Money("0.1", "EUR")
    c = Money("0.5", "EUR")
    d = Money("0.5", "USD")
    assert a > b
    assert (a < b) is False
    assert a >= b
    assert (a <= b) is False
    assert (a > c) is False
    assert (a < c) is False
    assert a >= c
    assert a <= c

    with pytest.raises(ValueError):
        is_smaller = c < d
    with pytest.raises(ValueError):
        is_smaller = c < d
    with pytest.raises(ValueError):
        is_equal = c == d
    assert (c < 1) is False
    assert (c > 1) is False


def test_currency():
    eur = Currency(
        name="Euro",
        code="EUR",
        numeric_code=123,
        symbol="€",
        exponent=2,
        entities=["Germany"],
        withdrawal_date=None,
        subunits=2,
    )
    usd = Currency(
        name="US Dollar",
        code="USD",
        numeric_code=456,
        symbol="$",
        exponent=2,
        entities=["United States of America"],
        withdrawal_date=None,
        subunits=2,
    )
    repr(eur)
    assert (eur == usd) is False
    assert (eur == 2) is False
    assert eur != usd
    with pytest.raises(ValueError):
        Currency(
            name=2,
            code="EUR",
            numeric_code=123,
            symbol="€",
            exponent=2,
            entities=["Germany"],
            withdrawal_date=None,
            subunits=2,
        )
    with pytest.raises(ValueError):
        Currency(
            name="Euro",
            code=2,
            numeric_code=123,
            symbol="€",
            exponent=2,
            entities=["Germany"],
            withdrawal_date=None,
            subunits=2,
        )
    with pytest.raises(ValueError):
        Currency(
            name="Euro",
            code="EUR",
            numeric_code=123,
            symbol="€",
            exponent="2",
            entities=["Germany"],
            withdrawal_date=None,
            subunits=2,
        )


def test_formatting():
    non_currency = Money("12.2", None)
    assert f"{non_currency}" == "12.20"
    assert f"{non_currency:0.2f,symbol}" == "12.20"
    assert f"{non_currency:0.2f,postsymbol}" == "12.20"
    assert f"{non_currency:0.2f,shortcode}" == "12.20"
    assert f"{non_currency:0.2f,postshortcode}" == "12.20"

    a = Money("12.20", "USD")
    assert f"{a}" == "12.20 USD"
    assert f"{a:0.2f,symbol}" == "$12.20"
    assert f"{a:0.2f,postsymbol}" == "12.20$"
    assert f"{a:0.2f,shortcode}" == "USD 12.20"
    assert f"{a:0.2f,postshortcode}" == "12.20 USD"


def test_gt_other_currency_fail():
    a = Money("12.45", "USD")
    b = Money("67.89", "EUR")
    with pytest.raises(ValueError) as exinfo:
        a > b
    error_msg = (
        "Left has currency=US Dollar, right has currency=Euro. "
        "You need to convert to the same currency first."
    )
    assert str(exinfo.value) == error_msg
