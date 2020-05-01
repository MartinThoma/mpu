#!/usr/bin/env python

"""Decorators which are not in `functools`."""

# Core Library
import functools
import warnings
from time import time


def timing(func):
    """Measure the execution time of a function call and print the result."""

    @functools.wraps(func)
    def wrap(*args, **kw):
        t0 = time()
        result = func(*args, **kw)
        t1 = time()
        print(
            "func:{!r} args:[{!r}, {!r}] took: {:2.4f} sec".format(
                func.__name__, args, kw, t1 - t0
            )
        )
        return result

    return wrap


def deprecated(func):
    """
    Mark functions as deprecated.

    It will result in a warning being emitted when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.__code__.co_filename,
            lineno=func.__code__.co_firstlineno + 1,
        )
        return func(*args, **kwargs)

    return new_func
