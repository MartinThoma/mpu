"""
Create and manipulate two-dimensional geometrical entities such as lines.

For more advanced use cases, see:

* `sympy.geometry <https://docs.sympy.org/latest/modules/geometry/index.html>`_
* `Shapely <https://pypi.org/project/Shapely/>`_
"""

# Core Library
import math
from typing import FrozenSet, List, Set, Tuple, Union

# First party
from mpu.datastructures import Interval

EPSILON = 0.000001


class Point:
    """
    A point in a 2-dimensional Euclidean space.

    Parameters
    ----------
    x : float
    y : float
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}|{self.y})"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class LineSegment:
    """
    A line segment a a 2-dimensional Euclidean space.

    Parameters
    ----------
    p1 : Point
    p2 : Point
    """

    def __init__(self, p1: Point, p2: Point, name: str = "LineSegment"):
        self.p1 = p1
        self.p2 = p2
        self.name = name

    def length(self) -> float:
        """Get the length of this line segment."""
        return ((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2) ** 0.5

    def is_point(self):
        """Check if this LineSegment is a point."""
        return self.p1 == self.p2

    def angle(self) -> float:
        """Get the angle of this line."""
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        theta = math.atan2(dy, dx)
        angle = math.degrees(theta)  # angle is in (-180, 180]
        if angle < 0:
            angle = 360 + angle
        return angle

    def _get_equation_parameters(self):
        if self.p1.x == self.p2.x:
            raise ValueError("is not a function")
        # y1 = m*x1 + t
        # y2 = m*x2 + t
        # => y1 = m*x1 + (y2-m*x2)
        # <=> m = (y1 - y2) /(x1-x2)
        #    t = y1 - m*x1
        y1 = self.p1.y
        y2 = self.p2.y
        x1 = self.p1.x
        x2 = self.p2.x
        m = (y1 - y2) / (x1 - x2)
        t = y1 - m * x1
        return m, t

    def simplify(self):
        """Simplify this line segment to a point, if possible."""
        if self.is_point():
            return self.p1
        if self.p1.x > self.p2.x:
            return LineSegment(p1=self.p2, p2=self.p1)
        else:
            return self

    def intersect(self, other) -> Union[None, "LineSegment", Point]:
        """
        Get the intersection between this LineSegment and another LineSegment.

        Parameters
        ----------
        other : LineSegment

        Returns
        -------
        intersection : Union[None, LineSegment, Point]
        """
        if not do_lines_intersect(self, other):
            return None
        if self.is_point():
            p1 = self.simplify()
            return p1  # we know they intersect
        elif other.is_point():
            return other.intersect(self)
        elif self.angle() == other.angle():
            # The overlap is a line segment or a point!
            if self.angle() in [90, 270]:
                # The line segment is not a function
                x = self.p1.x
                return _get_straight_line_intersection(
                    x, other.p1.y, other.p2.y, self.p1.y, self.p2.y
                )
            else:
                # The LineSegment is a function
                x_start = max(min(self.p1.x, self.p2.x), min(other.p1.x, other.p2.x))
                x_end = min(max(self.p1.x, self.p2.x), max(other.p1.x, other.p2.x))
                m, t = self._get_equation_parameters()
                p1 = Point(x_start, m * x_start + t)
                p2 = Point(x_end, m * x_end + t)
                return LineSegment(p1, p2)
        else:
            # We know that we have to real line segments, that those intersect
            # and that their angle is different. Hence the return value
            # must be a point
            if self.angle() in [90, 270]:
                x = self.p1.x

                if other.angle() in [90, 270]:
                    return _get_straight_line_intersection(
                        x, other.p1.y, other.p2.y, self.p1.y, self.p2.y
                    )
                else:
                    m, t = other._get_equation_parameters()
                    y = m * x + t
                    return Point(x, y)
            elif other.angle() in [90, 270]:
                x = other.p1.x
                m, t = self._get_equation_parameters()
                y = m * x + t
                return Point(x, y)
            else:
                # The overlap is a point
                m1, t1 = self._get_equation_parameters()
                m2, t2 = other._get_equation_parameters()
                # m1 * x + t1 = m2 * x + t2
                # <=> (m1 - m2) * x = t2 - t1
                # <=> x = (t2 - t1) / (m1 - m2)
                x = (t2 - t1) / (m1 - m2)
                y = m1 * x + t1
                return Point(x, y)

    def bounding_box(self) -> Tuple[Point, Point]:
        """
        Get the bounding box of this line represented by two points.

        The p1 point is in the lower left corner, the p2 one at the
        upper right corner.
        """
        result = (
            Point(min(self.p1.x, self.p2.x), min(self.p1.y, self.p2.y)),
            Point(max(self.p1.x, self.p2.x), max(self.p1.y, self.p2.y)),
        )
        return result

    def __str__(self) -> str:
        if self.name == "LineSegment":
            return f"LineSegment [{self.p1} to {self.p2}]"
        else:
            return self.name

    __repr__ = __str__

    def __hash__(self):
        return hash((self.p1, self.p2, self.name))

    def __eq__(self, other):
        if not isinstance(other, LineSegment):
            return False
        return self.name == other.name and (
            (self.p1 == other.p1 and self.p2 == other.p2)
            or (self.p1 == other.p2 and self.p2 == other.p1)
        )


def _get_straight_line_intersection(x, other_y1, other_y2, self_y1, self_y2):
    """Get the intersection point of two straight vertical lines."""
    self_y = Interval(left=min(self_y1, self_y2), right=max(self_y1, self_y2))
    other_y = Interval(left=min(other_y1, other_y2), right=max(other_y1, other_y2))

    intersection = self_y.intersection(other_y)
    if intersection.left == intersection.right:
        return Point(x, intersection.left)
    else:
        return LineSegment(Point(x, intersection.left), Point(x, intersection.right))


def do_bounding_boxes_intersect(a: Tuple[Point, Point], b: Tuple[Point, Point]) -> bool:
    """
    Check if bounding boxes do intersect.

    If one bounding box touches the other, they do intersect.
    """
    return (
        a[0].x <= b[1].x and a[1].x >= b[0].x and a[0].y <= b[1].y and a[1].y >= b[0].y
    )


def crossproduct(a: Point, b: Point) -> float:
    """Get the cross product of two points."""
    return a.x * b.y - b.x * a.y


def is_point_on_line(a: LineSegment, b: Point) -> bool:
    """Check if point b is on LineSegment a."""
    # Move the image, so that a.p1 is on (0|0)
    p2 = Point(a.p2.x - a.p1.x, a.p2.y - a.p1.y)
    a_tmp = LineSegment(Point(0, 0), p2)
    b_tmp = Point(b.x - a.p1.x, b.y - a.p1.y)
    r = crossproduct(a_tmp.p2, b_tmp)
    return abs(r) < EPSILON


def is_point_right_of_line(a: LineSegment, b: Point) -> bool:
    """Check if point b is right of line a."""
    # Move the image, so that a.p1 is on (0|0)
    a_tmp = LineSegment(Point(0, 0), Point(a.p2.x - a.p1.x, a.p2.y - a.p1.y))
    b_tmp = Point(b.x - a.p1.x, b.y - a.p1.y)
    return crossproduct(a_tmp.p2, b_tmp) < 0


def line_segment_touches_or_crosses_line(a: LineSegment, b: LineSegment) -> bool:
    """Check if line segment a touches or crosses line segment b."""
    return (
        is_point_on_line(a, b.p1)
        or is_point_on_line(a, b.p2)
        or (is_point_right_of_line(a, b.p1) ^ is_point_right_of_line(a, b.p2))
    )


def do_lines_intersect(a: LineSegment, b: LineSegment) -> bool:
    """Check if LineSegments a and b intersect."""
    box1 = a.bounding_box()
    box2 = b.bounding_box()
    return (
        do_bounding_boxes_intersect(box1, box2)
        and line_segment_touches_or_crosses_line(a, b)
        and line_segment_touches_or_crosses_line(b, a)
    )


def get_all_intersecting_lines_by_brute_force(
    lines: List[LineSegment],
) -> Set[FrozenSet[LineSegment]]:
    """
    Get all interectionLines by applying a brute force algorithm.

    Parameters
    ----------
    lines : all lines you want to check, in no order

    Returns
    -------
    a list that contains all pairs of intersecting lines
    """
    intersections: Set[FrozenSet[LineSegment]] = set()

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if do_lines_intersect(lines[i], lines[j]):
                tmp = frozenset({lines[i], lines[j]})
                intersections.add(tmp)
    return intersections
