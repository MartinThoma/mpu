# -*- coding: utf-8 -*-

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
    with multiprocessing.pool.ThreadPool(nb_threads) as pool:
        return pool.map(loop_function, parameters)
