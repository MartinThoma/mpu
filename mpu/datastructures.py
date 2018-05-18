#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility datastructures."""

# core modules
import collections


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
        for index, el in enumerate(self):
            if index not in indices:
                new_list.append(el)
        return EList(new_list)


def flatten(iterable):
    """
    Flatten an given iterable of iterables into one list.

    Parameters
    ----------
    iterable : iterable

    Returns
    -------
    flat_list : list

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
        if isinstance(item, collections.Iterable):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list
