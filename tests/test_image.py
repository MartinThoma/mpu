#!/usr/bin/env python

# Core Library
import sys
from unittest import mock

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


def test_import_error():
    path = "files/example.png"
    source = pkg_resources.resource_filename(__name__, path)
    with mock.patch.dict(sys.modules, {"PIL": None}):
        meta = get_meta(source)
    meta["file"] = None
    assert meta == {"file": None}
