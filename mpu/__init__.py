# -*- coding: utf-8 -*-

# core modules
import random
from pkg_resources import get_distribution
try:
    __version__ = get_distribution('mpu').version
except:
    __version__ = 'Not installed'


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
