"""Decorators which are not in `functools`."""
from functools import wraps
from time import time


def timing(f):
    """Measure the execution time of a function call and print the result."""
    @wraps(f)
    def wrap(*args, **kw):
        t0 = time()
        result = f(*args, **kw)
        t1 = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %
              (f.__name__, args, kw, t1 - t0))
        return result
    return wrap
