#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# core modules
import datetime as dt

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
