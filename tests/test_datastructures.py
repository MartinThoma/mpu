#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest

# internal modules
from mpu.datastructures import EList, flatten


class DatastructuresTest(unittest.TestCase):

    def test_EList_empty(self):
        elist = EList()
        self.assertEqual(len(elist), 0)

    def test_EList_getitem(self):
        elist = EList([2, 3, 5, 7, 11])
        self.assertEqual(elist[2], 5)
        self.assertEqual(elist[0], 2)
        self.assertEqual(elist[1], 3)
        self.assertEqual(elist[4], 11)

    def test_flatten_string(self):
        assert flatten(['foobar']) == ['foobar']
