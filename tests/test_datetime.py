#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Core Library
import unittest
from datetime import datetime

# Third party
import pytz

# First party
import mpu.datetime


class DatetimeTest(unittest.TestCase):

    def test_add_hour(self):
        tz = pytz.timezone('Europe/Berlin')
        out = mpu.datetime.add_time(datetime(1918, 4, 15, 0, 0,
                                             tzinfo=pytz.utc)
                                    .astimezone(tz),
                                    hours=1).isoformat()
        self.assertEqual(out, '1918-04-15T03:00:00+02:00')

    def test_generate_fail(self):
        with self.assertRaises(ValueError):
            mpu.datetime.generate(datetime(2018, 1, 1), datetime(2018, 1, 1))
