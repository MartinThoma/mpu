#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Mathematical functions."""


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
