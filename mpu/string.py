#!/usr/bin/env python

"""
String manipulation, verification and formatting.

For more complex checks, you might want to use the
[validators](http://validators.readthedocs.io) package.
"""

# Core Library
import socket
from email.utils import parseaddr
from typing import List, Optional, Union

# Third party
import pkg_resources

# First party
import mpu.io


def is_email(potential_email_address: str) -> bool:
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
    >>> is_email('Martin <>')
    False
    """
    context, mail = parseaddr(potential_email_address)
    first_condition = len(context) == 0
    dot_after_at = (
        "@" in potential_email_address and "." in potential_email_address.split("@")[1]
    )
    return first_condition and dot_after_at


def is_int(potential_int: str) -> bool:
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
    except ValueError:
        return False


def is_float(potential_float: str) -> bool:
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
    except ValueError:
        return False


def str2bool(string_: str, default="raise") -> bool:
    """
    Convert a string to a bool.

    Parameters
    ----------
    string_ : str
    default : {'raise', False}
        Default behaviour if none of the "true" strings is detected.

    Returns
    -------
    boolean : bool

    Examples
    --------
    >>> str2bool('True')
    True
    >>> str2bool('1')
    True
    >>> str2bool('0')
    False
    """
    true = ["true", "t", "1", "y", "yes", "enabled", "enable", "on"]
    false = ["false", "f", "0", "n", "no", "disabled", "disable", "off"]
    if string_.lower() in true:
        return True
    elif string_.lower() in false or (not default):
        return False
    else:
        raise ValueError("The value '{}' cannot be mapped to boolean.".format(string_))


def str2str_or_none(string_: str) -> Optional[str]:
    """
    Convert a string to a str or to None.

    Parameters
    ----------
    string_ : str

    Returns
    -------
    str_or_none : bool or None

    Examples
    --------
    >>> str2str_or_none('True')
    'True'
    >>> str2str_or_none('1')
    '1'
    >>> str2str_or_none('0')
    '0'
    >>> str2str_or_none('undefined')
    """
    if is_none(string_, default=False):
        return None
    else:
        return string_


def str2bool_or_none(string_: str, default="raise") -> Optional[bool]:
    """
    Convert a string to a bool or to None.

    Parameters
    ----------
    string_ : str
    default : {'raise', False}
        Default behaviour if none of the "true" or "none" strings is detected.

    Returns
    -------
    bool_or_none : bool or None

    Examples
    --------
    >>> str2bool_or_none('True')
    True
    >>> str2bool_or_none('1')
    True
    >>> str2bool_or_none('0')
    False
    >>> str2bool_or_none('undefined')
    """
    if is_none(string_, default=False):
        return None
    else:
        return str2bool(string_, default)


def str2float_or_none(string_: str) -> Optional[float]:
    """
    Convert a string to a float or to None.

    Parameters
    ----------
    string_ : str

    Returns
    -------
    float_or_none : float or None

    Examples
    --------
    >>> str2float_or_none('1')
    1.0
    >>> str2float_or_none('1.2')
    1.2
    >>> str2float_or_none('undefined')
    """
    if is_none(string_, default=False):
        return None
    else:
        return float(string_)


def str2int_or_none(string_: str) -> Optional[int]:
    """
    Convert a string to a int or to None.

    Parameters
    ----------
    string_ : str

    Returns
    -------
    int_or_none : int or None

    Examples
    --------
    >>> str2int_or_none('2')
    2
    >>> str2int_or_none('undefined')
    """
    if is_none(string_, default=False):
        return None
    else:
        return int(string_)


def is_none(string_: str, default="raise") -> bool:
    """
    Check if a string is equivalent to None.

    Parameters
    ----------
    string_ : str
    default : {'raise', False}
        Default behaviour if none of the "None" strings is detected.

    Returns
    -------
    is_none : bool

    Examples
    --------
    >>> is_none('2', default=False)
    False
    >>> is_none('undefined', default=False)
    True
    """
    none = ["none", "undefined", "unknown", "null", ""]
    if string_.lower() in none:
        return True
    elif not default:
        return False
    else:
        raise ValueError("The value '{}' cannot be mapped to none.".format(string_))


def is_iban(potential_iban: str) -> bool:
    """
    Check if a string is a valid IBAN number.

    IBAN is described in ISO 13616-1:2007 Part 1.

    Spaces are ignored.

    # CODE
    0 = always zero
    b = BIC or National Bank code
    c = Account number
    i = holder's kennitala (national identification number)
    k = IBAN check digits
    n = Branch number
    t = Account type
    x = National check digit or character

    Examples
    --------
    >>> is_iban('DE89 3704 0044 0532 0130 00')
    True
    >>> is_iban('DE89 3704 0044 0532 0130 01')
    False
    """
    path = "data/iban.csv"  # always use slash in Python packages
    filepath = pkg_resources.resource_filename("mpu", path)
    data = mpu.io.read(filepath, delimiter=";", format="dicts")
    potential_iban = potential_iban.replace(" ", "")  # Remove spaces
    if len(potential_iban) < min([int(el["length"]) for el in data]):
        return False
    country = None
    for element in data:
        if element["iban_fields"][:2] == potential_iban[:2]:
            country = element
            break
    if country is None:
        return False
    if len(potential_iban) != int(country["length"]):
        return False
    if country["country_en"] == "Germany":
        checksum_vals = [
            value
            for field_type, value in zip(country["iban_fields"], potential_iban)
            if field_type == "k"
        ]
        checksum_val = "".join(checksum_vals)
        checksum_exp = _calculate_german_iban_checksum(
            potential_iban, country["iban_fields"]
        )
        return checksum_val == checksum_exp
    return True


def is_ipv4(
    potential_ipv4: str,
    allow_leading_zeros: bool = False,
    allow_shortened_addresses=False,
) -> bool:
    """
    Check if a string is a valid IPv4 address.

    Parameters
    ----------
    potential_ipv4 : str

    Returns
    -------
    is_valid : bool

    Examples
    --------
    >>> is_ipv4("192.168.0.4")
    True
    >>> is_ipv4("192.168..4")
    False
    >>> is_ipv4("192.168.01.4", allow_leading_zeros=True)
    True
    >>> is_ipv4("192.168.01.4", allow_leading_zeros=False)
    False
    >>> is_ipv4("256.168.01.4")
    False
    >>> is_ipv4("4", allow_shortened_addresses=True)
    True
    >>> is_ipv4("4", allow_shortened_addresses=False)
    False
    """
    if not allow_shortened_addresses:
        if potential_ipv4.count(".") != 3:
            return False
    try:
        socket.inet_aton(potential_ipv4)
    except OSError:
        return False
    if allow_leading_zeros:
        return True
    else:
        return all(
            len(block) == 1 or block[0] != "0" for block in potential_ipv4.split(".")
        )


def _calculate_german_iban_checksum(
    iban: str, iban_fields: str = "DEkkbbbbbbbbcccccccccc"
) -> str:
    """
    Calculate the checksum of the German IBAN format.

    Examples
    --------
    >>> iban =        'DE41500105170123456789'
    >>> _calculate_german_iban_checksum(iban)
    '41'
    """
    numbers: List[str] = [
        value
        for field_type, value in zip(iban_fields, iban)
        if field_type in ["b", "c"]
    ]
    translate = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }
    for i in range(ord("A"), ord("Z") + 1):
        translate[chr(i)] = str(i - ord("A") + 10)
    for val in "DE00":
        translated = translate[val]
        for char in translated:
            numbers.append(char)
    number = sum(int(value) * 10 ** i for i, value in enumerate(numbers[::-1]))
    checksum = 98 - (number % 97)
    return str(checksum)


def human_readable_bytes(nb_bytes: Union[int, float], suffix: str = "B") -> str:
    """
    Convert a byte number into a human readable format.

    Parameters
    ----------
    nb_bytes : Union[int, float]
    suffix : str, optional (default: "B")

    Returns
    -------
    size_str : str

    Examples
    --------
    >>> human_readable_bytes(123)
    '123.0 B'

    >>> human_readable_bytes(1025)
    '1.0 KiB'

    >>> human_readable_bytes(9671406556917033397649423)
    '8.0 YiB'
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(nb_bytes) < 1024.0:
            return "{:3.1f} {}{}".format(nb_bytes, unit, suffix)
        nb_bytes /= 1024.0
    return "{:.1f} {}{}".format(nb_bytes, "Yi", suffix)
