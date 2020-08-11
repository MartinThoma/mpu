"""Machine Learning functions."""

# Core Library
from typing import Iterable, List

# First party
from mpu.math import argmax


def indices2one_hot(indices: Iterable, nb_classes: int) -> List:
    """
    Convert an iterable of indices to one-hot encoded list.

    You might also be interested in sklearn.preprocessing.OneHotEncoder

    Parameters
    ----------
    indices : Iterable
        iterable of indices
    nb_classes : int
        Number of classes
    dtype : type

    Returns
    -------
    one_hot : List

    Examples
    --------
    >>> indices2one_hot([0, 1, 1], 3)
    [[1, 0, 0], [0, 1, 0], [0, 1, 0]]
    >>> indices2one_hot([0, 1, 1], 2)
    [[1, 0], [0, 1], [0, 1]]
    """
    if nb_classes < 1:
        raise ValueError(f"nb_classes={nb_classes}, but positive number expected")

    one_hot = []
    for index in indices:
        one_hot.append([0] * nb_classes)
        one_hot[-1][index] = 1
    return one_hot


def one_hot2indices(one_hots: List) -> List:
    """
    Convert an iterable of one-hot encoded targets to a list of indices.

    Parameters
    ----------
    one_hot : List

    Returns
    -------
    indices : List

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
