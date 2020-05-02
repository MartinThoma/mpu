#!/usr/bin/env python

"""
Mathematical functions which are not adequately covered by standard libraries.

Standard libraries are:

* `math <https://docs.python.org/3/library/math.html>`_
* `scipy <https://docs.scipy.org/doc/scipy/reference/>`_
* `sympy <http://docs.sympy.org/latest/index.html>`_

"""


# Core Library
import math as math_stl
import operator
from functools import reduce


def generate_primes():
    """
    Generate an infinite sequence of prime numbers.

    The algorithm was originally written by David Eppstein, UC Irvine. See:
    http://code.activestate.com/recipes/117119/

    Examples
    --------
    >>> g = generate_primes()
    >>> next(g)
    2
    >>> next(g)
    3
    >>> next(g)
    5
    """
    divisors = {}  # map number to at least one divisor

    candidate = 2  # next potential prime

    while True:
        if candidate in divisors:
            # candidate is composite. divisors[candidate] is the list of primes
            # that divide it. Since we've reached candidate, we no longer need
            # it in the map, but we'll mark the next multiples of its witnesses
            # to prepare for larger numbers
            for p in divisors[candidate]:
                divisors.setdefault(p + candidate, []).append(p)
            del divisors[candidate]
        else:
            # candidate is a new prime
            yield candidate

            # mark its first multiple that isn't
            # already marked in previous iterations
            divisors[candidate * candidate] = [candidate]

        candidate += 1


def factorize(number):
    """
    Get the prime factors of an integer except for 1.

    Parameters
    ----------
    number : int

    Returns
    -------
    primes : iterable

    Examples
    --------
    >>> factorize(-17)
    [-1, 17]
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(3**25)
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    >>> factorize(1)
    [1]
    """
    if not isinstance(number, int):
        raise ValueError("integer expected, but type(number)={}".format(type(number)))
    if number < 0:
        return [-1] + factorize(number * (-1))
    elif number == 0:
        raise ValueError("All primes are prime factors of 0.")
    else:
        for i in range(2, int(math_stl.ceil(number ** 0.5)) + 1):
            if number % i == 0:
                if i == number:
                    return [i]
                else:
                    return [i] + factorize(int(number / i))
        return [number]


def is_prime(number):
    """
    Check if a number is prime.

    Parameters
    ----------
    number : int

    Returns
    -------
    is_prime_number : bool

    Examples
    --------
    >>> is_prime(-17)
    False
    >>> is_prime(17)
    True
    >>> is_prime(47055833459)
    True
    """
    return len(factorize(number)) == 1


def product(iterable, start=1):
    """
    Calculate the product of the iterables.

    Parameters
    ----------
    iterable : iterable
        List, tuple or similar which contains numbers
    start : number, optional (default: 1)

    Returns
    -------
    product : number

    Examples
    --------
    >>> product([1, 2, 3, 4, 5])
    120
    >>> product([])
    1
    """
    return reduce(operator.mul, iterable, start)


def argmax(iterable):
    """
    Find the first index of the biggest value in the iterable.

    Parameters
    ----------
    iterable : iterable

    Returns
    -------
    argmax : int

    Examples
    --------
    >>> argmax([0, 0, 0])
    0
    >>> argmax([1, 0, 0])
    0
    >>> argmax([0, 1, 0])
    1
    >>> argmax([])
    """
    max_value = None
    max_index = None
    for index, value in enumerate(iterable):
        if (max_value is None) or max_value < value:
            max_value = value
            max_index = index
    return max_index


def round_up(x, decimal_places):
    """
    Round a float up to decimal_places.

    Parameters
    ----------
    x : float
    decimal_places : int

    Returns
    -------
    rounded_float : float

    Examples
    --------
    >>> round_up(1.2344, 3)
    1.235
    >>> round_up(1.234, 3)
    1.234
    >>> round_up(1.23456, 3)
    1.235
    >>> round_up(1.23456, 2)
    1.24
    """
    return round(x + 5 * 10 ** (-1 * (decimal_places + 1)), decimal_places)


def round_down(x, decimal_places):
    """
    Round a float down to decimal_places.

    Parameters
    ----------
    x : float
    decimal_places : int

    Returns
    -------
    rounded_float : float

    Examples
    --------
    >>> round_down(1.23456, 3)
    1.234
    >>> round_down(1.23456, 2)
    1.23
    """
    from math import floor

    d = int("1" + ("0" * decimal_places))
    return floor(x * d) / d


def gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor.

    Currently, this uses the Euclidean algorithm.

    Parameters
    ----------
    a : int
        Non-zero
    b : int

    Returns
    -------
    greatest_common_divisor : int

    Examples
    --------
    >>> gcd(1, 7)
    1
    >>> gcd(-1, -1)
    1
    >>> gcd(1337, 42)
    7
    >>> gcd(-1337, -42)
    7
    >>> gcd(120, 364)
    4
    >>> gcd(273, 1870)
    1
    """
    if a == 0 or b == 0:
        raise ValueError("gcd(a={a}, b={b}) is undefined")
    while b != 0:
        a, b = b, a % b
    return abs(a)
