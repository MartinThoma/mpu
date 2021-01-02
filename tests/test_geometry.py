# Core Library
import math
import random
from typing import List, Set

# Third party
import hypothesis.strategies as st
import pytest
from hypothesis import given

# First party
from mpu.geometry import (
    EPSILON,
    LineSegment,
    Point,
    _get_straight_line_intersection,
    crossproduct,
    do_bounding_boxes_intersect,
    do_lines_intersect,
    get_all_intersecting_lines_by_brute_force,
    is_point_right_of_line,
    line_segment_touches_or_crosses_line,
)


@given(st.floats(min_value=0.0, max_value=360.0))
def test_angle(angle: float):
    epsilon = 0.0001
    x = math.cos(math.radians(angle))
    y = math.sin(math.radians(angle))
    ls = LineSegment(Point(0, 0), Point(x, y))
    assert abs(ls.angle() - angle) < epsilon


def test_antisymmetry_of_cross_product():
    points = [Point(0, 0), Point(1, 1)]
    for _ in range(50):
        points.append(Point(random.random(), random.random()))

    for p1 in points:
        for p2 in points:
            r1 = crossproduct(p1, p2)
            r2 = crossproduct(p2, p1)
            assert abs(r1 + r2) < EPSILON, f"[{p1}, {p2}]"


def test_point_str():
    p1 = Point(0, 0)
    assert str(p1) == "(0|0)"
    assert repr(p1) == "(0|0)"


def test_point_equality():
    p1 = Point(0, 0)
    assert not (p1 == "(0|0)")

    p2 = Point(0.0, 0.0)
    assert p1 == p2


def test_line_segment_simplify():
    line_segment1 = LineSegment(Point(42, 0), Point(0, 0))
    assert str(line_segment1.simplify()) == "LineSegment [(0|0) to (42|0)]"


def test_line_segment_simplify_self():
    line_segment1 = LineSegment(Point(0, 0), Point(42, 0))
    assert str(line_segment1.simplify()) == "LineSegment [(0|0) to (42|0)]"


def test_line_segment_equality():
    line_segment1 = LineSegment(Point(0, 0), Point(42, 0))
    line_segment2 = LineSegment(Point(42, 0), Point(0, 0))
    assert line_segment1 == line_segment2

    line_segment1 = LineSegment(Point(0, 0), Point(42.1, 0))
    line_segment2 = LineSegment(Point(42, 0), Point(0, 0))
    assert line_segment1 != line_segment2

    assert line_segment1 != "[(0|0), (42|0)]"


def test_line_segment_no_intersection1():
    """No intersection"""
    ls1 = LineSegment(Point(0, 0), Point(1, 0))
    ls2 = LineSegment(Point(2, 0), Point(3, 0))
    assert ls1.intersect(ls2) is None
    assert ls2.intersect(ls1) is None


def test_line_segment_no_intersection2():
    """No intersection"""
    ls1 = LineSegment(Point(0, 0), Point(0, 1))
    ls2 = LineSegment(Point(0, 2), Point(0, 3))
    assert ls1.intersect(ls2) is None
    assert ls2.intersect(ls1) is None


def test_line_segment_intersection_90_270():
    """A single point intersection"""
    ls1 = LineSegment(Point(0, 0), Point(0, 1))
    ls2 = LineSegment(Point(0, 3), Point(0, 1))
    assert ls1.intersect(ls2) == Point(0, 1)
    assert ls2.intersect(ls1) == Point(0, 1)


def test_line_segment_point_intersection():
    """A single point intersection"""
    ls1 = LineSegment(Point(0, 0), Point(0, 1))
    ls2 = LineSegment(Point(0, 1), Point(0, 3))
    assert ls1.intersect(ls2) == Point(0, 1)
    assert ls2.intersect(ls1) == Point(0, 1)


def test_line_segment_point_intersection1():
    """A single point intersection"""
    ls1 = LineSegment(Point(0, 0), Point(1, 1))
    ls2 = LineSegment(Point(1, 1), Point(3, 3))
    assert ls1.intersect(ls2).simplify() == Point(1, 1)
    assert ls2.intersect(ls1).simplify() == Point(1, 1)


def test_line_segment_point_intersection2():
    """A single point intersection"""
    ls1 = LineSegment(Point(0, 0), Point(1, 1))
    ls2 = LineSegment(Point(1, 1), Point(1, 1))
    assert ls1.intersect(ls2) == Point(1, 1)
    assert ls2.intersect(ls1) == Point(1, 1)


def test_line_segment_point_intersection3():
    """A single point intersection"""
    ls1 = LineSegment(Point(5, 0), Point(5, 10))
    ls2 = LineSegment(Point(0, 0), Point(20, 20))
    assert ls1.intersect(ls2) == Point(5, 5)
    assert ls2.intersect(ls1) == Point(5, 5)


def test_line_segment_point_intersection4():
    """A single point intersection"""
    ls1 = LineSegment(Point(0, 4), Point(20, 4))
    ls2 = LineSegment(Point(0, 0), Point(20, 20))
    assert ls1.intersect(ls2) == Point(4, 4)
    assert ls2.intersect(ls1) == Point(4, 4)


def test_line_segment_point_intersection_horizontal_vertical_cross():
    """A single point intersection"""
    ls1 = LineSegment(Point(-4, 0), Point(4, 0))
    ls2 = LineSegment(Point(0, -4), Point(0, 4))
    assert ls1.intersect(ls2) == Point(0, 0)
    assert ls2.intersect(ls1) == Point(0, 0)


def test_line_segment_point_intersection_up_down():
    """A single point intersection"""
    ls1 = LineSegment(Point(0, -4), Point(0, 4))
    ls2 = LineSegment(Point(0, 2), Point(0, -2))
    expected = LineSegment(Point(0, -2), Point(0, 2))
    assert ls1.intersect(ls2).simplify() == expected
    assert ls2.intersect(ls1).simplify() == expected


def test_line_segment_length_x():
    line_segment = LineSegment(Point(0, 0), Point(42, 0))
    assert line_segment.length() == 42

    line_segment = LineSegment(Point(2, 0), Point(42, 0))
    assert line_segment.length() == 40


def test_line_segment_length_y():
    line_segment = LineSegment(Point(0, 0), Point(0, 42))
    assert line_segment.length() == 42

    line_segment = LineSegment(Point(0, 2), Point(0, 42))
    assert line_segment.length() == 40


def test_line_segment_length_xy():
    line_segment = LineSegment(Point(0, 0), Point(3, 4))
    assert line_segment.length() == 5


def test_line_segment_angle_zero():
    line_segment = LineSegment(Point(0, 0), Point(1, 0))
    assert line_segment.angle() == 0


def test_line_segment_angle_180():
    line_segment = LineSegment(Point(0, 0), Point(-1, 0))
    assert line_segment.angle() == 180


@given(
    st.floats(min_value=-1, max_value=1),
    st.floats(min_value=-1, max_value=1),
    st.floats(min_value=-1, max_value=1),
    st.floats(min_value=-1, max_value=1),
)
def test_line_segment_angle_boundaries(x1, y1, x2, y2):
    line_segment = LineSegment(Point(x1, y1), Point(x2, y2))
    assert 0 <= line_segment.angle() < 360


def test_get_equation_parameters():
    line_segment = LineSegment(Point(0, 0), Point(1, 0))
    assert line_segment._get_equation_parameters() == (0, 0)

    line_segment = LineSegment(Point(0, 0), Point(1, 1))
    assert line_segment._get_equation_parameters() == (1, 0)

    line_segment = LineSegment(Point(0, 0), Point(0, 1))
    with pytest.raises(ValueError) as exinfo:
        line_segment._get_equation_parameters()
    assert str(exinfo.value) == "The given points have the same x-coordinate"


def test_point_right_of_line():
    line = LineSegment(Point(0, 0), Point(0, 7))
    a = Point(5, 5)
    assert is_point_right_of_line(line, a)


def test_point_left_of_line():
    line = LineSegment(Point(0, 0), Point(0, 7))
    a = Point(-5, 5)
    assert not is_point_right_of_line(line, a)


def test_point_on_line():
    line = LineSegment(Point(0, 0), Point(4, 4))
    a = Point(3, 3)
    assert not is_point_right_of_line(line, a)

    line = LineSegment(Point(4, 4), Point(0, 0))
    assert not is_point_right_of_line(line, a)


def test_bounding_boxes_intersect_t1():
    a = (Point(0, 0), Point(5, 5))
    b = (Point(1, 1), Point(2, 2))
    assert do_bounding_boxes_intersect(a, b)


def test_bounding_boxes_intersect_t2():
    a = (Point(0, 0), Point(3, 3))
    b = (Point(1, -1), Point(2, 7))
    assert do_bounding_boxes_intersect(a, b)


def test_bounding_boxes_intersect_t3():
    a = (Point(0, 0), Point(3, 3))
    b = (Point(1, -1), Point(2, 2))
    assert do_bounding_boxes_intersect(a, b)


def test_bounding_boxes_intersect_t4():
    a = (Point(0, 0), Point(3, 3))
    b = (Point(3, 3), Point(5, 5))
    assert do_bounding_boxes_intersect(a, b)


def test_bounding_boxes_intersect_f1():
    a = (Point(0, 0), Point(3, 3))
    b = (Point(4, 4), Point(5, 5))
    assert not do_bounding_boxes_intersect(a, b)


def test_line_segment_crosses_line():
    """Tests for lineSegmentCrossesLine"""
    line_segment = LineSegment(Point(5, 5), Point(17, 17))
    line = LineSegment(Point(0, 0), Point(1, 1))
    assert line_segment_touches_or_crosses_line(line_segment, line)

    line_segment = LineSegment(Point(17, 17), Point(5, 5))
    line = LineSegment(Point(0, 0), Point(1, 1))
    assert line_segment_touches_or_crosses_line(line_segment, line)


def test_lines_dont_intersect_f1():
    """Tests for do_lines_intersect"""
    a = LineSegment(Point(0, 0), Point(7, 7))
    b = LineSegment(Point(3, 4), Point(4, 5))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f2():
    a = LineSegment(Point(-4, 4), Point(-2, 1))
    b = LineSegment(Point(-2, 3), Point(0, 0))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f3():
    a = LineSegment(Point(0, 0), Point(0, 1))
    b = LineSegment(Point(2, 2), Point(2, 3))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f4():
    a = LineSegment(Point(0, 0), Point(0, 1))
    b = LineSegment(Point(2, 2), Point(3, 2))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f5():
    a = LineSegment(Point(-1, -1), Point(2, 2))
    b = LineSegment(Point(3, 3), Point(5, 5))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f6():
    a = LineSegment(Point(0, 0), Point(1, 1))
    b = LineSegment(Point(2, 0), Point(0.5, 2))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f7():
    a = LineSegment(Point(1, 1), Point(4, 1))
    b = LineSegment(Point(2, 2), Point(3, 2))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intersect_f8():
    a = LineSegment(Point(0, 5), Point(6, 0))
    b = LineSegment(Point(2, 1), Point(2, 2))
    assert not do_lines_intersect(a, b)


def test_lines_do_intersect_t1():
    a = LineSegment(Point(0, -2), Point(0, 2))
    b = LineSegment(Point(-2, 0), Point(2, 0))
    assert do_lines_intersect(a, b)


def test_lines_do_intersect_t2():
    a = LineSegment(Point(5, 5), Point(0, 0))
    b = LineSegment(Point(1, 1), Point(8, 2))
    assert do_lines_intersect(a, b)


def test_lines_do_intersect_t3():
    a = LineSegment(Point(-1, 0), Point(0, 0))
    b = LineSegment(Point(-1, -1), Point(-1, 1))
    assert do_lines_intersect(a, b)


def test_lines_do_intersect_t4():
    a = LineSegment(Point(0, 2), Point(2, 2))
    b = LineSegment(Point(2, 0), Point(2, 4))
    assert do_lines_intersect(a, b)


def test_lines_do_intersect_t5():
    a = LineSegment(Point(0, 0), Point(5, 5))
    b = LineSegment(Point(1, 1), Point(3, 3))
    assert do_lines_intersect(a, b)


def test_lines_do_intersect_t6():
    for _ in range(50):
        ax = random.random()
        ay = random.random()
        bx = random.random()
        by = random.random()
        a = LineSegment(Point(ax, ay), Point(bx, by))
        b = LineSegment(Point(ax, ay), Point(bx, by))
        assert do_lines_intersect(a, b)


def test_blog_example():
    """check getAllIntersectingLines()"""
    lines: List[LineSegment] = [
        LineSegment(Point(1, 4), Point(6, 1), "a"),
        LineSegment(Point(2, 1), Point(5, 4), "b"),
        LineSegment(Point(3, 1), Point(6, 4), "c"),
        LineSegment(Point(4, 1), Point(8, 5), "d"),
        LineSegment(Point(3, 4), Point(9, 3), "e"),
        LineSegment(Point(7, 2), Point(9, 3), "f"),
        LineSegment(Point(6, 7), Point(9, 1), "g"),
        LineSegment(Point(11, 1), Point(16, 5), "h"),
        LineSegment(Point(13, 3), Point(13, 4), "i"),
        LineSegment(Point(15, 3), Point(15, 4), "j"),
        LineSegment(Point(13, 2), Point(14, 2), "k"),
        LineSegment(Point(14, 1), Point(14, 2), "l"),
        LineSegment(Point(17, 3), Point(21, 3), "m"),
        LineSegment(Point(19, 5), Point(19, 1), "n"),
        LineSegment(Point(11, 1), Point(16, 5), "o"),
    ]

    intersections: Set[LineSegment] = set()
    add = frozenset({lines[0], lines[1]})
    intersections.add(add)
    add = frozenset({lines[0], lines[2]})
    intersections.add(add)
    add = frozenset({lines[0], lines[3]})
    intersections.add(add)
    add = frozenset({lines[3], lines[6]})
    intersections.add(add)
    add = frozenset({lines[4], lines[1]})
    intersections.add(add)
    add = frozenset({lines[4], lines[2]})
    intersections.add(add)
    add = frozenset({lines[4], lines[3]})
    intersections.add(add)
    add = frozenset({lines[4], lines[5]})
    intersections.add(add)
    add = frozenset({lines[4], lines[6]})
    intersections.add(add)
    add = frozenset({lines[5], lines[6]})
    intersections.add(add)
    add = frozenset({lines[10], lines[11]})
    intersections.add(add)
    add = frozenset({lines[12], lines[13]})
    intersections.add(add)
    add = frozenset({lines[7], lines[14]})
    intersections.add(add)

    intersectionsBrute: Set[LineSegment] = get_all_intersecting_lines_by_brute_force(
        lines
    )
    # intersectionsSweep: Set[LineSegment] = getAllIntersectingLines(lines)

    assert intersectionsBrute == intersections

    # twice [e,g], but not [[d, g], [e, c], [e, d], [e, f]]
    # assert intersectionsSweep == intersections


def test_compare_to_brute_force():
    n = 30
    max_intersections = (n * n - n) / 2

    lines: List[LineSegment] = []
    for _ in range(n):
        a = Point(random.random(), random.random())
        b = Point(random.random(), random.random())
        lines.append(LineSegment(a, b))

    intersectionsBrute: Set[LineSegment] = get_all_intersecting_lines_by_brute_force(
        lines
    )
    # intersectionsSweep: Set[LineSegment] = getAllIntersectingLines(lines)
    assert len(intersectionsBrute) <= max_intersections
    # assert intersectionsBrute == intersectionsSweep


def test_get_straight_line_intersection():
    intersection = _get_straight_line_intersection(0, 0, 10, 5, 20)
    assert intersection == LineSegment(Point(0, 5), Point(0, 10))
