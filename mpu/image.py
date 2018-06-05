#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Image manipulation."""


def get_meta(filepath):
    """
    Get meta-information of an image.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    meta : dict
    """
    meta = {}
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            width, height = img.size
        meta['width'] = width
        meta['height'] = height
    except ImportError:
        pass
    try:
        import scipy.ndimage
        height, width, channels = scipy.ndimage.imread(filepath).shape
        meta['width'] = width
        meta['height'] = height
        meta['channels'] = channels
    except ImportError:
        pass
    return meta
