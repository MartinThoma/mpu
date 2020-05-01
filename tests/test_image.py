#!/usr/bin/env python

# Third party
import pkg_resources

# First party
from mpu.image import get_meta


def test_get_meta():
    path = "files/example.png"
    source = pkg_resources.resource_filename(__name__, path)
    meta = get_meta(source)
    meta["file"] = None
    assert meta == {"width": 252, "height": 167, "channels": 4, "file": None}
