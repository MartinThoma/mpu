#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Datetime related utility functions."""

from __future__ import absolute_import

# core modules
import datetime as dt
import random

# 3rd party modules
import pytz


def add_time(datetime_obj, days=0, hours=0, minutes=0, seconds=0):
    """
    Add time to a timezone-aware datetime object.

    This keeps the timezone correct, even if it changes due to daylight
    saving time (DST).

    Parameters
    ----------
    datetime_obj : datetime.datetime
    days : int
    hours : int
    minutes : int
    seconds : int

    Returns
    -------
    datetime : datetime.datetime
    """
    seconds += minutes * 60
    seconds += hours * 60**2
    seconds += days * 24 * 60**2
    t14 = datetime_obj + dt.timedelta(seconds=seconds)  # Invalid timezone!
    t14 = t14.astimezone(pytz.utc).astimezone(t14.tzinfo)  # Fix the timezone
    return t14


def generate(minimum, maximum, local_random=random.Random()):
    """
    Generate a random date.

    The generated dates are uniformly distributed.

    Parameters
    ----------
    minimum : datetime object
    maximum : datetime object
    local_random : random.Random

    Returns
    -------
    generated_date : datetime object

    Examples
    --------
    >>> import random; r = random.Random(); r.seed(0)
    >>> from datetime import datetime

    >>> generate(datetime(2018, 1, 1), datetime(2018, 1, 2), local_random=r)
    datetime.datetime(2018, 1, 1, 20, 15, 58, 47972)

    >>> generate(datetime(2018, 1, 1), datetime(2018, 1, 2), local_random=r)
    datetime.datetime(2018, 1, 1, 18, 11, 27, 260414)
    """
    if not (minimum < maximum):
        raise ValueError('{} is not smaller than {}'.format(minimum, maximum))

    # Python 3 allows direct multiplication of timedelta with a float, but
    # Python 2.7 does not. Hence this work-around.
    time_d = maximum - minimum
    time_d_float = time_d.total_seconds()
    time_d_rand = dt.timedelta(seconds=time_d_float * local_random.random())
    generated = minimum + time_d_rand
    return generated
