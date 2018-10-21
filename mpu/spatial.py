#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for spatial datastructures."""

# internal modules
from mpu.math import product


class Point(object):
    """Point in R^n."""

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def nb_dimensions(self):
        """Give the number of dimensions this point."""
        return len(self.coordinates)

    def __getitem__(self, key):
        return self.coordinates.__getitem__(key)


class AABB(object):
    """
    Axis-Aligned Bounding Box.

    Parameters
    ----------
    point1 : Point
    point2 : Point
    """

    def __init__(self, point1, point2):
        if point1.nb_dimensions() != point2.nb_dimensions():
            raise ValueError('point1.nb_dimensions()={}, '
                             'point2.nb_dimensions()={}'
                             .format(point1, point2))
        self.p1 = point1
        self.p2 = point2

    def area(self):
        """
        Calculate the area of this AABB.

        Examples
        --------
        >>> aabb = AABB(Point([0, 0]), Point([3, 3]))
        >>> aabb.area()
        9
        """
        differences = [(self.p2[i] - self.p1[i])
                       for i in range(self.p1.nb_dimensions())]
        return product(differences)
