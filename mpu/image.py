#!/usr/bin/env python

"""Image manipulation."""

# Core Library
from typing import Dict

# First party
import mpu


def get_meta(filepath: str) -> Dict:
    """
    Get meta-information of an image.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    meta : Dict
    """
    meta = {}
    try:
        from PIL import Image

        with Image.open(filepath) as img:
            width, height = img.size
        meta["width"] = width
        meta["height"] = height
        meta["channels"] = len(img.mode)  # RGB, RGBA - does this always work?
    except ImportError:
        pass

    # Get times - creation, last edit, last open
    meta["file"] = mpu.io.get_file_meta(filepath)
    return meta
