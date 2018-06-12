#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Decorators which are not in `functools`."""

# core modules
from time import time
import functools
import sys
import warnings


def timing(func):
    """Measure the execution time of a function call and print the result."""
    @functools.wraps(func)
    def wrap(*args, **kw):
        t0 = time()
        result = func(*args, **kw)
        t1 = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %
              (func.__name__, args, kw, t1 - t0))
        return result
    return wrap


def deprecated(func):
    """
    Mark functions as deprecated.

    It will result in a warning being emitted when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        if sys.version_info < (3, 0):
            warnings.warn_explicit(
                "Call to deprecated function {}.".format(func.__name__),
                category=DeprecationWarning,
                filename=func.func_code.co_filename,
                lineno=func.func_code.co_firstlineno + 1
            )
        else:
            warnings.warn_explicit(
                "Call to deprecated function {}.".format(func.__name__),
                category=DeprecationWarning,
                filename=func.__code__.co_filename,
                lineno=func.__code__.co_firstlineno + 1
            )
        return func(*args, **kwargs)
    return new_func
