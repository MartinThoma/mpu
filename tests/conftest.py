# Core Library
import os
from tempfile import mkstemp

# Third party
import pytest


def create_tempfile(suffix=None, prefix=None):
    """Named"""
    handle, pathname = mkstemp(suffix=suffix, prefix=prefix)
    os.close(handle)
    return pathname


@pytest.fixture
def json_tempfile():
    pathname = create_tempfile(suffix=".json")
    yield pathname
    os.remove(pathname)


@pytest.fixture
def jsonl_tempfile():
    pathname = create_tempfile(suffix=".jsonl")
    yield pathname
    os.remove(pathname)


@pytest.fixture
def jpg_tempfile():
    pathname = create_tempfile(suffix=".jpg")
    yield pathname
    os.remove(pathname)


@pytest.fixture
def pickle_tempfile():
    pathname = create_tempfile(suffix=".pickle")
    yield pathname
    os.remove(pathname)


@pytest.fixture
def csv_tempfile():
    pathname = create_tempfile(suffix=".csv")
    yield pathname
    os.remove(pathname)


@pytest.fixture
def hdf5_tempfile():
    pathname = create_tempfile(suffix=".hdf5")
    yield pathname
    os.remove(pathname)
