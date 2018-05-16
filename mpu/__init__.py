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
    >>> munich = (48.1372, 11.5756)
    >>> berlin = (52.5186, 13.4083)
    >>> round(haversine_distance(munich, berlin), 1)
    504.2

    >>> new_york_city = (40.712777777778, -74.005833333333)  # NYC
    >>> round(haversine_distance(berlin, new_york_city), 1)
    6385.3
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    if not (-90.0 <= lat1 <= 90):
        raise ValueError('lat1={:2.2f}, but must be in [-90,+90]'.format(lat1))
    if not (-90.0 <= lat2 <= 90):
        raise ValueError('lat2={:2.2f}, but must be in [-90,+90]'.format(lat1))
    if not (-180.0 <= lon1 <= 180):
        raise ValueError('lon1={:2.2f}, but must be in [-180,+180]'
                         .format(lat1))
    if not (-180.0 <= lon2 <= 180):
        raise ValueError('lon1={:2.2f}, but must be in [-180,+180]'
                         .format(lat1))
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d
