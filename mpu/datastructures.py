#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility datastructures."""

# core modules
import collections
from copy import deepcopy


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
        is_iterable = (isinstance(item, collections.Iterable) and
                       (string_flattening or
                        (not string_flattening and not isinstance(item, str))
                        ))
        if is_iterable:
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


def dict_merge(dict_left, dict_right, merge_method='take_left_shallow'):
    """
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
    new_dict = {}
    if merge_method in ['take_right_shallow', 'take_right_deep']:
        return _dict_merge_right(dict_left, dict_right, merge_method)
    elif merge_method == 'take_left_shallow':
        return dict_merge(dict_right, dict_left, 'take_right_shallow')
    elif merge_method == 'take_left_deep':
        return dict_merge(dict_right, dict_left, 'take_right_deep')
    elif merge_method == 'sum':
        new_dict = deepcopy(dict_left)
        for key, value in dict_right.items():
            if key not in new_dict:
                new_dict[key] = value
            else:
                recurse = isinstance(value, dict)
                if recurse:
                    new_dict[key] = dict_merge(dict_left[key],
                                               dict_right[key],
                                               merge_method='sum')
                else:
                    new_dict[key] = dict_left[key] + dict_right[key]
        return new_dict
    else:
        raise NotImplementedError('merge_method=\'{}\' is not known.'
                                  .format(merge_method))


def _dict_merge_right(dict_left, dict_right, merge_method):
    """See documentation of mpu.datastructures.dict_merge."""
    new_dict = deepcopy(dict_left)
    for key, value in dict_right.items():
        if key not in new_dict:
            new_dict[key] = value
        else:
            recurse = (merge_method == 'take_right_deep' and
                       isinstance(dict_left[key], dict) and
                       isinstance(dict_right[key], dict))
            if recurse:
                new_dict[key] = dict_merge(dict_left[key],
                                           dict_right[key],
                                           merge_method='take_right_deep')
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
    >>> d = {'a': {'b': 'c', 'd': 'e'}}
    >>> expected = {'a': {'b': 'foobar', 'd': 'e'}}
    >>> set_dict_value(d, ['a', 'b'], 'foobar') == expected
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
