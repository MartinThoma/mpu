#!/usr/bin/env python

"""Functions for path manipultion and retrival of files."""

# Core Library
import os

# Third party
import pkg_resources


def get_all_files(root, followlinks=False):
    """
    Get all files within the given root directory.

    Note that this list is not ordered.

    Parameters
    ----------
    root : str
        Path to a directory
    followlinks : bool, optional (default: False)

    Returns
    -------
    filepaths : list
        List of absolute paths to files
    """
    filepaths = []
    for path, _, files in os.walk(root, followlinks=followlinks):
        for name in files:
            filepaths.append(os.path.abspath(os.path.join(path, name)))
    return filepaths


def get_from_package(package_name, path):
    """
    Get the absolute path to a file in a package.

    Parameters
    ----------
    package_name : str
        e.g. 'mpu'
    path : str
        Path within a package

    Returns
    -------
    filepath : str
    """
    filepath = pkg_resources.resource_filename(package_name, path)
    return os.path.abspath(filepath)
