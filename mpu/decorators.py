"""Decorators which are not in `functools`."""

# Core Library
import functools
import warnings
from time import time
from typing import Callable, Dict, List


def timing(func: Callable) -> Callable:
    """Measure the execution time of a function call and print the result."""

    @functools.wraps(func)
    def wrap(*args: List, **kw: Dict) -> Callable:
        t0 = time()
        result = func(*args, **kw)
        t1 = time()
        print(
            f"func:{func.__name__!r} args:[{args!r}, {kw!r}] took: "
            f"{t1 - t0:2.4f} sec"
        )
        return result

    return wrap


def deprecated(func: Callable) -> Callable:
    """
    Mark functions as deprecated.

    It will result in a warning being emitted when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args: List, **kwargs: Dict) -> Callable:
        warnings.warn_explicit(
            f"Call to deprecated function {func.__name__}.",
            category=DeprecationWarning,
            filename=func.__code__.co_filename,
            lineno=func.__code__.co_firstlineno + 1,
        )
        return func(*args, **kwargs)

    return new_func
