#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu import parallel_for, haversine_distance


class DatastructuresInit(unittest.TestCase):

    def test_parallel_for(self):
        import time

        def looping_function(payload):
            i, j = payload
            time.sleep(1)
            return i + j
        parameters = list((i, i + 1) for i in range(50))
        out = parallel_for(looping_function, parameters)
        self.assertEquals(out, [2 * i + 1 for i in range(50)])

    def test_haversine(self):
        with self.assertRaises(ValueError):
            haversine_distance((-200, 0), (0, 0))
        with self.assertRaises(ValueError):
            haversine_distance((0, -200), (0, 0))
        with self.assertRaises(ValueError):
            haversine_distance((0, 0), (-200, 0))
        with self.assertRaises(ValueError):
            haversine_distance((0, 0), (0, -200))
