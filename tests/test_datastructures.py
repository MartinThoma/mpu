#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
import unittest
from datetime import datetime

# 3rd party modules
import pytest

# internal modules
from mpu.datastructures import EList, flatten, Interval, IntervalUnion


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
        assert flatten(["foobar"]) == ["foobar"]


def test_interval_creation_successes():
    a = Interval(0, 1)
    assert str(a) == "[0, 1]"

    b = Interval(0.0, 1.0)
    assert str(b) == "[0.0, 1.0]"

    c = Interval(datetime(2000, 1, 1), datetime(2000, 1, 2))
    assert str(c) == "[2000-01-01 00:00:00, 2000-01-02 00:00:00]"

    d = Interval(None, None)
    assert str(d) == "[]"

    e = Interval()
    assert str(e) == "[]"


def test_interval_creation_fail_left_bigger():
    with pytest.raises(RuntimeError):
        Interval(1, -1)


def test_interval_creation_fail_left_none():
    with pytest.raises(RuntimeError):
        Interval(None, -1)


def test_interval_creation_fail_right_none():
    with pytest.raises(RuntimeError):
        Interval(1, None)


def test_interval_equality():
    assert Interval(42, 1337) == Interval(42, 1337)
    assert Interval(None, None) == Interval(None, None)


def test_interval_inequality():
    assert Interval(0, 0) != 0
    assert Interval(None, None) != Interval(0, 0)
    assert Interval(0, 0) != Interval(None, None)
    assert Interval(42, 1337) != Interval(3141, 5000)


def test_interval_union():
    i01 = Interval(0, 1)
    assert Interval(None, None).union(Interval(42, 1337)) == Interval(42, 1337)
    assert Interval(42, 1337).union(Interval(None, None)) == Interval(42, 1337)
    assert i01.union(Interval(1, 3)) == Interval(0, 3)
    assert i01.union(Interval(2, 4)) == IntervalUnion([[0, 1], [2, 4]])
    assert i01.union(Interval(3, 5)) == IntervalUnion([[0, 1], [3, 5]])
    assert i01.union(Interval(-1, 6)) == Interval(-1, 6)
    assert Interval(1, 3).union(Interval(2, 4)) == Interval(1, 4)
    assert Interval(1, 3).union(Interval(3, 5)) == Interval(1, 5)
    assert Interval(1, 3).union(Interval(-1, 6)) == Interval(-1, 6)
    assert Interval(2, 4).union(Interval(3, 5)) == Interval(2, 5)
    assert Interval(2, 4).union(Interval(-1, 6)) == Interval(-1, 6)
    assert Interval(3, 5).union(Interval(-1, 6)) == Interval(-1, 6)


def test_interval_intersection():
    i42 = Interval(42, 1337)
    assert Interval(None, None).intersection(i42) == Interval(None, None)
    assert i42.intersection(Interval(None, None)) == Interval(None, None)
    assert Interval(0, 1).intersection(Interval(1, 3)) == Interval(1, 1)
    assert Interval(0, 1).intersection(Interval(2, 4)) == Interval(None, None)
    assert Interval(0, 1).intersection(Interval(3, 5)) == Interval(None, None)
    assert Interval(0, 1).intersection(Interval(-1, 6)) == Interval(0, 1)
    assert Interval(1, 3).intersection(Interval(2, 4)) == Interval(2, 3)
    assert Interval(1, 3).intersection(Interval(3, 5)) == Interval(3, 3)
    assert Interval(1, 3).intersection(Interval(-1, 6)) == Interval(1, 3)
    assert Interval(2, 4).intersection(Interval(3, 5)) == Interval(3, 4)
    assert Interval(2, 4).intersection(Interval(-1, 6)) == Interval(2, 4)
    assert Interval(3, 5).intersection(Interval(-1, 6)) == Interval(3, 5)
    assert Interval(1, 10).intersection(Interval(-1, 12)) == Interval(1, 10)


def test_interval_issubset():
    assert Interval(1, 2).issubset(Interval(0, 10))
    assert Interval(0, 2).issubset(Interval(0, 10))
    assert Interval(0, 10).issubset(Interval(0, 10))


def test_interval_issubset_not():
    assert not Interval(-1, 2).issubset(Interval(0, 10))
    assert not Interval(0, 11).issubset(Interval(0, 10))
    assert not Interval(-1, 11).issubset(Interval(0, 10))
    assert not Interval(-2, -1).issubset(Interval(0, 10))


def test_interval_issubset_error():
    with pytest.raises(Exception):
        Interval(0, 1).issubset([0, 1])


def test_interval_union_simplification_empty():
    iu = IntervalUnion([])
    iu._simplify()
    assert iu.intervals == []


def test_interval_union_simplification_disjunct():
    iu = IntervalUnion([[0, 1], [42, 1337]])
    iu._simplify()
    assert iu.intervals == [Interval(0, 1), Interval(42, 1337)]


def test_interval_union_simplification_one_point_connected():
    iu = IntervalUnion([[0, 1], [1, 1337]])
    iu._simplify()
    assert iu.intervals == [Interval(0, 1337)]


def test_interval_union_simplification_overlap_connected():
    iu = IntervalUnion([[0, 3], [1, 1337]])
    iu._simplify()
    assert iu.intervals == [Interval(0, 1337)]


def test_interval_union_simplification_three_step_connected():
    iu = IntervalUnion([[0, 1], [2, 3], [4, 5], [1, 1337]])
    iu._simplify()
    assert iu.intervals == [Interval(0, 1337)]


def test_interval_union_union_1():
    iu1 = IntervalUnion([[0, 1], [2, 3], [4, 5]])
    iu2 = IntervalUnion([[1, 2], [3, 4]])
    iu3 = iu1.union(iu2)
    assert iu3.intervals == [Interval(0, 5)]


def test_interval_union_union_2():
    iu1 = IntervalUnion([[0, 1], [2, 3], [4, 5]])
    iu2 = IntervalUnion([[-2, -1], [3.5, 3.7]])
    iu3 = iu1.union(iu2)
    assert iu3.intervals == [
        Interval(-2, -1),
        Interval(0, 1),
        Interval(2, 3),
        Interval(3.5, 3.7),
        Interval(4, 5),
    ]


def test_interval_union_union_interval():
    iu1 = IntervalUnion([[0, 1], [2, 3], [4, 5]])
    iu2 = Interval(6, 7)
    iu3 = iu1.union(iu2)
    assert iu3.intervals == [
        Interval(0, 1),
        Interval(2, 3),
        Interval(4, 5),
        Interval(6, 7),
    ]


def test_interval_union_union_error():
    iu1 = IntervalUnion([[0, 1], [2, 3], [4, 5]])
    iu2 = [[-2, -1], [3.5, 3.7]]
    with pytest.raises(RuntimeError):
        iu1.union(iu2)


def test_interval_union_intersection_1():
    iu1 = IntervalUnion([[0, 100]])
    iu2 = IntervalUnion([[1, 2]])
    iu3 = iu1.intersection(iu2)
    assert iu3.intervals == [Interval(1, 2)]


def test_interval_union_intersection_2():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = IntervalUnion([[5, 25], [45, 60]])
    iu3 = iu1.intersection(iu2)
    iu_expected = [Interval(5, 10), Interval(20, 25), Interval(45, 50)]
    assert iu3.intervals == iu_expected


def test_interval_union_intersection_3():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = IntervalUnion([[10, 20]])
    iu3 = iu1.intersection(iu2)
    assert iu3.intervals == [Interval(10, 10), Interval(20, 20)]


def test_interval_union_intersection():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = IntervalUnion([[-1, 60]])
    iu3 = iu1.intersection(iu2)
    expected_intervals = [Interval(0, 10), Interval(20, 30), Interval(40, 50)]
    assert iu3.intervals == expected_intervals


def test_interval_union_intersection_error():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = [[-1, 60]]
    with pytest.raises(RuntimeError):
        iu1.intersection(iu2)


def test_interval_union_issubset_equal():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    assert iu1.issubset(iu2)
    assert iu2.issubset(iu1)


def test_interval_union_issubset_part():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = IntervalUnion([[20, 30], [40, 50]])
    assert not iu1.issubset(iu2)
    assert iu2.issubset(iu1)


def test_interval_union_issubset_error():
    iu = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    with pytest.raises(Exception):
        assert iu.issubset([[0, 100]])


def test_interval_union_inequality():
    iu1 = IntervalUnion([[0, 10], [20, 30], [40, 50]])
    iu2 = [[0, 10], [20, 30], [40, 50]]
    assert iu1 != iu2


def test_interval_union_equality():
    iu1 = IntervalUnion([[0, 10]])
    iu2 = Interval(0, 10)
    assert iu1 == iu2


def test_interval_union_is_empty():
    iu = IntervalUnion([[], [], []])
    assert iu.is_empty()
