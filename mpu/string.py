#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
String manipulation and verification.

For more complex checks, you might want to use the
[validators](http://validators.readthedocs.io) package.
"""

# core modules
from email.utils import parseaddr


def is_email(potential_email_address):
    """
    Check if potential_email_address is a valid e-mail address.

    Please note that this function has no false-negatives but many
    false-positives. So if it returns that the input is not a valid
    e-mail adress, it certainly isn't. If it returns True, it might still be
    invalid. For example, the domain could not be registered.

    Parameters
    ----------
    potential_email_address : str

    Returns
    -------
    is_email : bool

    Examples
    --------
    >>> is_email('')
    False
    >>> is_email('info@martin-thoma.de')
    True
    >>> is_email('info@math.martin-thoma.de')
    True
    >>> is_email('Martin Thoma <info@martin-thoma.de>')
    False
    >>> is_email('info@martin-thoma')
    False
    """
    context, mail = parseaddr(potential_email_address)
    first_condition = len(context) == 0 and len(mail) != 0
    dot_after_at = ('@' in potential_email_address and
                    '.' in potential_email_address.split('@')[1])
    return first_condition and dot_after_at


def is_int(potential_int):
    """
    Check if potential_int is a valid integer.

    Parameters
    ----------
    potential_int : str

    Returns
    -------
    is_int : bool

    Examples
    --------
    >>> is_int('123')
    True
    >>> is_int('1234567890123456789')
    True
    >>> is_int('0')
    True
    >>> is_int('-123')
    True
    >>> is_int('123.45')
    False
    >>> is_int('a')
    False
    >>> is_int('0x8')
    False
    """
    try:
        int(potential_int)
        return True
    except:
        return False


def is_float(potential_float):
    """
    Check if potential_float is a valid float.

    Returns
    -------
    is_float : bool

    Examples
    --------
    >>> is_float('123')
    True
    >>> is_float('1234567890123456789')
    True
    >>> is_float('0')
    True
    >>> is_float('-123')
    True
    >>> is_float('123.45')
    True
    >>> is_float('a')
    False
    >>> is_float('0x8')
    False
    """
    try:
        float(potential_float)
        return True
    except:
        return False
