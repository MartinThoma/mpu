#!/usr/bin/env python

"""Reading and writing common file formats."""

# core modules
import csv
import json
import os

# internal modules
from mpu.datastructures import EList


def read(filepath, **kwargs):
    """
    Read a file.

    Supported formats:

    * CSV
    * JSON

    Parameters
    ----------
    filepath : str
        Path to the file that should be read.
    kwargs : dict
        Any keywords for the specific file format.

    Returns
    -------
    data : str or bytes
    """
    if filepath.lower().endswith('.csv'):
        with open(filepath, 'r') as fp:
            if 'delimiter' not in kwargs:
                kwargs['delimiter'] = ','
            if 'quotechar' not in kwargs:
                kwargs['quotechar'] = '"'
            if 'skiprows' not in kwargs:
                kwargs['skiprows'] = []
            if isinstance(kwargs['skiprows'], int):
                kwargs['skiprows'] = [i for i in range(kwargs['skiprows'])]
            reader = csv.reader(fp,
                                delimiter=kwargs['delimiter'],
                                quotechar=kwargs['quotechar'])
            data = EList([row for row in reader])
            data = data.remove_indices(kwargs['skiprows'])
        return data
    elif filepath.lower().endswith('.json'):
        with open(filepath) as data_file:
            data = json.load(data_file)
        return data
    else:
        raise NotImplementedError('File \'{}\' is not known.'.format(filepath))


def download(source, sink=None):
    """
    Download a file.

    Parameters
    ----------
    source : str
        Where the file comes from. Some URL.
    sink : str or None (default: same filename in current directory)
        Where the file gets stored. Some filepath in the local file system.
    """
    try:
        from urllib.request import urlretrieve  # Python 3
    except ImportError:
        from urllib import urlretrieve  # Python 2
    if sink is None:
        sink = os.path.abspath(os.path.split(source)[1])
    urlretrieve(source, sink)
    return sink
