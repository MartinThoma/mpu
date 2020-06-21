#!/usr/bin/env python

"""Utility datastructures."""

# Core Library
import collections
import logging
from copy import deepcopy

# First party
from mpu.datastructures.trie import Trie  # noqa

logger = logging.getLogger(__name__)


class EList(list):
    """
    Enhanced List.

    This class supports every operation a normal list supports. Additionally,
    you can call it with a list as an argument.

    Examples
    --------
    >>> l = EList([2, 1, 0])
    >>> l[2]
    0
    >>> l[[2, 0]]
    [0, 2]
    >>> l[l]
    [0, 1, 2]
    """

    def __init__(self, *args):
        list.__init__(self, *args)

    def __getitem__(self, key):
        """
        Retrieve one or multiple elements.

        Parameters
        ----------
        key : int or List[int]

        Returns
        -------
        value : EList or element
        """
        if isinstance(key, list):
            return EList([self[index] for index in key])
        else:
            return list.__getitem__(self, key)

    def remove_indices(self, indices):
        """
        Remove rows by which have the given indices.

        Parameters
        ----------
        indices : list

        Returns
        -------
        filtered_list : EList
        """
        new_list = []
        for index, element in enumerate(self):
            if index not in indices:
                new_list.append(element)
        return EList(new_list)


def flatten(iterable, string_flattening=False):
    """
    Flatten an given iterable of iterables into one list.

    Parameters
    ----------
    iterable : iterable
    string_flattening : bool
        If this is False, then strings are NOT flattened

    Returns
    -------
    flat_list : List

    Examples
    --------
    >>> flatten([1, [2, [3]]])
    [1, 2, 3]

    >>> flatten(((1, 2), (3, 4), (5, 6)))
    [1, 2, 3, 4, 5, 6]

    >>> flatten(EList([EList([1, 2]), (3, [4, [[5]]])]))
    [1, 2, 3, 4, 5]
    """
    flat_list = []
    for item in iterable:
        is_iterable = isinstance(item, collections.abc.Iterable) and (
            string_flattening or (not isinstance(item, str))
        )
        if is_iterable:
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


def dict_merge(dict_left, dict_right, merge_method="take_left_shallow"):
    r"""
    Merge two dictionaries.

    This method does NOT modify dict_left or dict_right!

    Apply this method multiple times if the dictionary is nested.

    Parameters
    ----------
    dict_left : dict
    dict_right: dict
    merge_method : {'take_left_shallow', 'take_left_deep', \
                    'take_right_shallow', 'take_right_deep', \
                    'sum'}
        * take_left_shallow: Use both dictinaries. If both have the same key,
          take the value of dict_left
        * take_left_deep : If both dictionaries have the same key and the value
          is a dict for both again, then merge those sub-dictionaries
        * take_right_shallow : See take_left_shallow
        * take_right_deep : See take_left_deep
        * sum : sum up both dictionaries. If one does not have a value for a
          key of the other, assume the missing value to be zero.

    Returns
    -------
    merged_dict : dict

    Examples
    --------
    >>> dict_merge({'a': 1, 'b': 2}, {'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    True

    >>> out = dict_merge({'a': {'A': 1}},
    ...                  {'a': {'A': 2, 'B': 3}}, 'take_left_deep')
    >>> expected = {'a': {'A': 1, 'B': 3}}
    >>> out == expected
    True

    >>> out = dict_merge({'a': {'A': 1}},
    ...                  {'a': {'A': 2, 'B': 3}}, 'take_left_shallow')
    >>> expected = {'a': {'A': 1}}
    >>> out == expected
    True

    >>> out = dict_merge({'a': 1, 'b': {'c': 2}},
    ...                  {'b': {'c': 3, 'd': 4}},
    ...                  'sum')
    >>> expected = {'a': 1, 'b': {'c': 5, 'd': 4}}
    >>> out == expected
    True
    """
    if merge_method in ["take_right_shallow", "take_right_deep"]:
        return _dict_merge_right(dict_left, dict_right, merge_method)
    elif merge_method == "take_left_shallow":
        return dict_merge(dict_right, dict_left, "take_right_shallow")
    elif merge_method == "take_left_deep":
        return dict_merge(dict_right, dict_left, "take_right_deep")
    elif merge_method == "sum":
        new_dict = deepcopy(dict_left)
        for key, value in dict_right.items():
            if key not in new_dict:
                new_dict[key] = value
            else:
                recurse = isinstance(value, dict)
                if recurse:
                    new_dict[key] = dict_merge(
                        dict_left[key], dict_right[key], merge_method="sum"
                    )
                else:
                    new_dict[key] = dict_left[key] + dict_right[key]
        return new_dict
    else:
        raise NotImplementedError(
            "merge_method='{}' is not known.".format(merge_method)
        )


def _dict_merge_right(dict_left, dict_right, merge_method):
    """See documentation of mpu.datastructures.dict_merge."""
    new_dict = deepcopy(dict_left)
    for key, value in dict_right.items():
        if key not in new_dict:
            new_dict[key] = deepcopy(value)
        else:
            recurse = (
                merge_method == "take_right_deep"
                and isinstance(dict_left[key], dict)
                and isinstance(dict_right[key], dict)
            )
            if recurse:
                new_dict[key] = dict_merge(
                    dict_left[key], dict_right[key], merge_method="take_right_deep",
                )
            else:
                new_dict[key] = value
    return new_dict


def set_dict_value(dictionary, keys, value):
    """
    Set a value in a (nested) dictionary by defining a list of keys.

    .. note:: Side-effects
              This function does not make a copy of dictionary, but directly
              edits it.

    Parameters
    ----------
    dictionary : dict
    keys : List[Any]
    value : object

    Returns
    -------
    dictionary : dict

    Examples
    --------
    >>> d = {'a': {'b': {'c': 'x', 'f': 'g'}, 'd': 'e'}}
    >>> expected = {'a': {'b': {'c': 'foobar', 'f': 'g'}, 'd': 'e'}}
    >>> set_dict_value(d, ['a', 'b', 'c'], 'foobar') == expected
    True
    """
    orig = dictionary
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value
    return orig


def does_keychain_exist(dict_, list_):
    """
    Check if a sequence of keys exist in a nested dictionary.

    Parameters
    ----------
    dict_ : Dict[str/int/tuple, Any]
    list_ : List[str/int/tuple]

    Returns
    -------
    keychain_exists : bool

    Examples
    --------
    >>> d = {'a': {'b': {'c': 'd'}}}
    >>> l_exists = ['a', 'b']
    >>> does_keychain_exist(d, l_exists)
    True

    >>> l_no_existant = ['a', 'c']
    >>> does_keychain_exist(d, l_no_existant)
    False
    """
    for key in list_:
        if key not in dict_:
            return False
        dict_ = dict_[key]
    return True


class IntervalLike:
    """
    Anything like an interval or a union of an interval.

    As mpu supports Python 2.7 until 2020 and does not want to include extra
    dependencies, ABC cannot be used.
    """

    def is_empty(self):
        """Return if the IntervalLike is empty."""
        raise NotImplementedError()

    def issubset(self, other):
        """
        Check if the interval "self" is completely inside of other.

        Parameters
        ----------
        other : IntervalLike

        Returns
        -------
        is_inside : bool
        """

    def union(self, other):
        """
        Combine two Intervals.

        Parameters
        ----------
        other : IntervalLike

        Returns
        -------
        interval_union : IntervalLike
        """
        raise NotImplementedError()

    def intersection(self, other):
        """
        Intersect two IntervalLike objects.

        Parameters
        ----------
        other : IntervalLike

        Returns
        -------
        intersected : IntervalLike
        """


class Interval(IntervalLike):
    """
    Representation of an interval.

    The empty interval is represented as left=None, right=None.
    Left and right have to be comparable.
    Typically, it would be numbers or dates.

    Parameters
    ----------
    left : object
    right : object
    """

    def __init__(self, left=None, right=None):
        if int(left is None) + int(right is None) not in [0, 2]:
            raise RuntimeError("Either left and right are None, or neither.")
        elif (left is not None) and (left > right):
            raise RuntimeError("left may not be bigger than right")
        self.left = left
        self.right = right

    def is_empty(self):
        """Return if the interval is empty."""
        return self.left is None

    def union(self, other):
        """
        Combine two Intervals.

        Parameters
        ----------
        other : IntervalLike

        Returns
        -------
        interval_union : IntervalLike
        """
        # Capture special cases
        if self.is_empty():
            return other
        elif other.is_empty():
            return self

        # Standardize - after this step, the other.left is left of self.left
        if other.left > self.left:
            other, self = self, other

        # Go through all cases
        if other.right < self.left:
            # Completely disjunct
            return IntervalUnion([self, other])
        elif other.right == self.left:
            # next to each other
            return Interval(other.left, self.right)
        elif other.right <= self.right:
            return Interval(other.left, self.right)
        elif other.right > self.right:
            # other is a superset of self
            return other
        else:
            # This should never happen
            raise NotImplementedError(f"Can't merge {self} and {other}")

    def intersection(self, other):
        """
        Intersect two IntervalLike objects.

        Parameters
        ----------
        other : IntervalLike

        Returns
        -------
        intersected : IntervalLike
        """
        # Any intersection with an empty interval is empty
        if self.is_empty() or other.is_empty():
            return Interval(None, None)

        if isinstance(other, IntervalUnion):
            return other.intersection(self)

        # Standardize - after this step, the other.left is left of self.left
        if other.left > self.left:
            other, self = self, other

        # Go through all cases
        if other.right < self.left:
            # Completely disjunct
            return Interval(None, None)
        elif other.right == self.left:
            # next to each other
            return Interval(other.right, other.right)
        elif other.right <= self.right:
            return Interval(self.left, other.right)
        elif other.right > self.right:
            # other is a superset of self
            return self
        else:
            # This should never happen
            raise NotImplementedError(f"Can't intersect {self} and {other}")

    def __repr__(self):
        """Get an unambiguous representation."""
        if self.is_empty():
            return "Interval()"
        else:
            return "Interval({}, {})".format(self.left, self.right)

    def __str__(self):
        """Get an human-readable representation."""
        if self.is_empty():
            return "[]"
        else:
            return "[{}, {}]".format(self.left, self.right)

    __and__ = intersection
    __or__ = union

    def __eq__(self, other):
        """Check if other is equal to this object."""
        if isinstance(other, (Interval, IntervalUnion)):
            return self.issubset(other) and other.issubset(self)
        else:
            return False

    def issubset(self, other):
        """
        Check if the interval "self" is completely inside of other.

        Parameters
        ----------
        other : IntervalLike

        Returns
        -------
        is_inside : bool
        """
        if self.is_empty():
            return True
        elif other.is_empty():
            # This could only be true, if self was empty as well
            # The order of those if / elif blocks matters here!
            return False
        elif isinstance(other, Interval):
            return other.left <= self.left <= self.right <= other.right
        elif isinstance(other, IntervalUnion):
            for interval in other.intervals:
                if self.issubset(interval):
                    return True
            return
        else:
            raise RuntimeError(
                "issubset is only defined on Interval and "
                "IntervalUnion, "
                "but {} was given".format(type(other))
            )


class IntervalUnion(IntervalLike):
    """A union of Intervals."""

    def __init__(self, intervals):
        if not isinstance(intervals, list):
            raise TypeError("'{}' is not a list".format(type(intervals)))
        self.intervals = []
        for interval in intervals:
            if isinstance(interval, Interval):
                self.intervals.append(interval)
            else:
                if len(interval) == 0:
                    self.intervals.append(Interval())
                else:
                    self.intervals.append(Interval(interval[0], interval[1]))

    def is_empty(self):
        """Return if the IntervalUnion is empty."""
        for interval in self.intervals:
            if not interval.is_empty():
                return False
        return True

    def issubset(self, other):
        """
        Check if this IntervalUnion is completely inside of `other`.

        Parameters
        ----------
        other : Interval or IntervalUnion

        Returns
        -------
        is_inside : bool
        """
        self._simplify()
        if isinstance(other, Interval):
            # If every interval of this is inside the interval `other`,
            # then this IntervalUnion is completely in `other`.
            for interval in self.intervals:
                if not interval.issubset(other):
                    return False
            return True
        elif isinstance(other, IntervalUnion):
            for interval in self.intervals:
                if not interval.issubset(other):
                    return False
            return True
        else:
            raise RuntimeError(
                "issubset is only defined on Interval and "
                "IntervalUnion, "
                "but {} was given".format(type(other))
            )

    def _get_keypoints(self):
        """
        Get all points which are relevant for this IntervalUnion.

        Returns
        -------
        keypoints : List[object]
        """
        keypoints = []
        for interval in self.intervals:
            keypoints.append(interval.left)
            keypoints.append(interval.right)
        return keypoints

    def _simplify(self):
        """
        Simplify the representation of the components.

        This means:
            1. Making sure that the minimum number of components is used
            2. The intervals are in order (by left element)

        Returns
        -------
        simplified_interval_union : IntervalUnion
            Please note that this is guaranteed to stay an IntervalUnion, even
            if it collapses to a single interval.
        """
        if len(self.intervals) == 0:
            return
        self.intervals = sorted(self.intervals, key=lambda n: n.left)
        simpler_intervals = [self.intervals[0]]
        for interval in self.intervals[1:]:
            combined = simpler_intervals[-1].union(interval)
            if isinstance(combined, Interval):
                simpler_intervals[-1] = combined
            else:
                simpler_intervals.append(interval)
        self.intervals = simpler_intervals

    def union(self, other):
        """
        Return the union between this IntervalUnion and another object.

        Parameters
        ----------
        other : Interval or IntervalUnion

        Returns
        -------
        union : Interval or IntervalUnion
        """
        if isinstance(other, Interval):
            self.intervals.append(other)
        elif isinstance(other, IntervalUnion):
            self.intervals += other.intervals
        else:
            raise RuntimeError("Union with type={} not supported".format(type(other)))
        self._simplify()
        return self

    def intersection(self, other):
        """
        Return the intersection between this IntervalUnion and another object.

        This changes the object itself!

        Parameters
        ----------
        other : Interval or IntervalUnion

        Returns
        -------
        intersection : Interval or IntervalUnion
        """
        if isinstance(other, Interval):
            self.intervals = [
                interval.intersection(other) for interval in self.intervals
            ]
            self._simplify()
            return self
        elif isinstance(other, IntervalUnion):
            keypoints_self = sorted(self._get_keypoints())
            keypoints_other = sorted(other._get_keypoints())
            keypoints = sorted(keypoints_self + keypoints_other)
            new_intervals = []
            for i in range(len(keypoints) - 1):
                left, right = keypoints[i], keypoints[i + 1]
                interval = Interval(left, right)
                if interval.issubset(self) and interval.issubset(other):
                    new_intervals.append(interval)
            return IntervalUnion(new_intervals)
        else:
            raise RuntimeError(
                "Intersection with type={} not supported".format(type(other))
            )

    def __repr__(self):
        """Get an unambiguous representation."""
        return "IntervalUnion(" + str(self.intervals) + ")"

    def __str__(self):
        return str(self.intervals)

    def __eq__(self, other):
        """Check if other is equal to this object."""
        if isinstance(other, (IntervalUnion, Interval)):
            return self.issubset(other) and other.issubset(self)
        else:
            return False

    __and__ = intersection
    __or__ = union
