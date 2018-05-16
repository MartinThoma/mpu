# -*- coding: utf-8 -*-

# core modules
import random
import math

# internal modules
from mpu._version import __version__
from mpu import units, io, shell


def parallel_for(loop_function, parameters, nb_threads=100):
    """
    Execute the loop body in parallel.

    Parameters
    ----------
    loop_function : Python function which takes a tuple as input
    parameters : List of tuples
        Each element here should be executed in parallel.

    Returns
    -------
    return_values : list of return values
    """
    import multiprocessing.pool
    from contextlib import closing
    with closing(multiprocessing.pool.ThreadPool(nb_threads)) as pool:
        return pool.map(loop_function, parameters)


def consistent_shuffle(*lists):
    """
    Shuffle lists consistently.

    Parameters
    ----------
    *lists
        Variable length number of lists

    Returns
    -------
    shuffled_lists : tuple of lists
        All of the lists are shuffled consistently

    Examples
    --------
    >>> import mpu, random; random.seed(8)
    >>> mpu.consistent_shuffle([1,2,3], ['a', 'b', 'c'], ['A', 'B', 'C'])
    ([3, 2, 1], ['c', 'b', 'a'], ['C', 'B', 'A'])
    """
    perm = list(range(len(lists[0])))
    random.shuffle(perm)
    lists = tuple([lists[i][index] for index in perm]
                  for i in range(len(lists)))
    return lists


def haversine_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(haversine_distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d
