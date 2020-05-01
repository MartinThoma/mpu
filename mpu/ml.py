#!/usr/bin/env python

"""Machine Learning functions."""


# First party
from mpu.math import argmax


def indices2one_hot(indices, nb_classes):
    """
    Convert an iterable of indices to one-hot encoded list.

    You might also be interested in sklearn.preprocessing.OneHotEncoder

    Parameters
    ----------
    indices : iterable
        iterable of indices
    nb_classes : int
        Number of classes
    dtype : type

    Returns
    -------
    one_hot : list

    Examples
    --------
    >>> indices2one_hot([0, 1, 1], 3)
    [[1, 0, 0], [0, 1, 0], [0, 1, 0]]
    >>> indices2one_hot([0, 1, 1], 2)
    [[1, 0], [0, 1], [0, 1]]
    """
    if nb_classes < 1:
        raise ValueError(
            "nb_classes={}, but positive number expected".format(nb_classes)
        )

    one_hot = []
    for index in indices:
        one_hot.append([0] * nb_classes)
        one_hot[-1][index] = 1
    return one_hot


def one_hot2indices(one_hots):
    """
    Convert an iterable of one-hot encoded targets to a list of indices.

    Parameters
    ----------
    one_hot : list

    Returns
    -------
    indices : list

    Examples
    --------
    >>> one_hot2indices([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    [0, 1, 2]

    >>> one_hot2indices([[1, 0], [1, 0], [0, 1]])
    [0, 0, 1]
    """
    indices = []
    for one_hot in one_hots:
        indices.append(argmax(one_hot))
    return indices
