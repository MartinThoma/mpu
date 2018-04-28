# core modules
import unittest

# internal modules
from mpu.datastructures import EList


class DatastructuresTest(unittest.TestCase):

    def test_EList_empty(self):
        EList()

    def test_EList_getitem(self):
        l = EList([2, 3, 5, 7, 11])
        self.assertEqual(l[2], 5)
        self.assertEqual(l[0], 2)
        self.assertEqual(l[1], 3)
        self.assertEqual(l[4], 11)
