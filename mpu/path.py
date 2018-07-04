#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for path manipultion and retrival of files."""

# core modules
import os


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
