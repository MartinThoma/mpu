#!/usr/bin/env python

"""Test the mpu.io module."""

# Core Library
import datetime
import os
import sys
from unittest import mock

# Third party
import pkg_resources
import pytest

# First party
import mpu.io
from mpu.io import (
    _write_jsonl,
    download,
    get_file_meta,
    gzip_file,
    read,
    urlread,
    write,
)


def test_download_with_path(jpg_tempfile):
    source = (
        "https://upload.wikimedia.org/wikipedia/commons/e/e9/"
        "Aurelia-aurita-3-1-style.jpg"
    )
    download(source, jpg_tempfile)
    assert os.path.getsize(jpg_tempfile) == 116087


def test_get_file_meta():
    path = "files/example.json"
    source = pkg_resources.resource_filename(__name__, path)
    with mock.patch.dict(sys.modules, {"magic": None}):
        meta = get_file_meta(source)
    meta["filepath"] = None
    meta["last_access_datetime"] = None
    meta["modification_datetime"] = None

    # Exists on Windows, but not on Linux
    meta["creation_datetime"] = None

    expected = {
        "filepath": None,
        "creation_datetime": None,
        "last_access_datetime": None,
        "modification_datetime": None,
    }
    assert meta == expected


def test_urlread():
    url = "http://example.com"
    sample = urlread(url)
    assert sample.startswith("<!doctype html>")


def test_download_without_path():
    source = (
        "https://upload.wikimedia.org/wikipedia/commons/e/e9/"
        "Aurelia-aurita-3-1-style.jpg"
    )
    sink = download(source)
    download(source, sink)
    assert os.path.getsize(sink) == 116087
    os.remove(sink)  # cleanup of mkstemp


def test_read_csv():
    path = "files/example.csv"
    source = pkg_resources.resource_filename(__name__, path)
    data_real = read(source)
    data_exp = [
        ["a", "b", "c"],  # 0
        ["1", "A towel,", "1.0"],  # 1
        ["42", " it says, ", "2.0"],  # 2
        ["1337", "is about the most ", "-1"],  # 3
        ["0", "massively useful thing ", "123"],  # 4
        ["-2", "an interstellar hitchhiker can have.\n", "3"],  # 5
        ["3.141", "Special char test: €üößł", "2.7"],  # 6
    ]
    assert len(data_real) == len(data_exp)
    assert data_real[0] == data_exp[0]
    assert data_real[1] == data_exp[1]
    assert data_real[2] == data_exp[2]
    assert data_real[3] == data_exp[3]
    assert data_real[4] == data_exp[4]
    assert data_real[5] == data_exp[5]
    assert data_real[6] == data_exp[6]
    assert data_real == data_exp
    data_real = read(source, skiprows=1)
    assert data_real == data_exp[1:]
    data_real = read(source, skiprows=1, delimiter=",", quotechar='"')
    assert data_real == data_exp[1:]


def test_read_csv_dicts():
    path = "files/example.csv"
    source = pkg_resources.resource_filename(__name__, path)
    data_real = read(source, format="dicts")
    data_exp = [
        {"a": "1", "b": "A towel,", "c": "1.0"},
        {"a": "42", "b": " it says, ", "c": "2.0"},
        {"a": "1337", "b": "is about the most ", "c": "-1"},
        {"a": "0", "b": "massively useful thing ", "c": "123"},
        {"a": "-2", "b": "an interstellar hitchhiker can have.\n", "c": "3"},
        {"a": "3.141", "b": "Special char test: €üößł", "c": "2.7"},
    ]
    assert len(data_real) == len(data_exp)
    assert data_real[0] == data_exp[0]
    assert data_real == data_exp


def test_write_csv(csv_tempfile):
    data = [
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\n", "3"],
    ]
    write(csv_tempfile, data)
    data_read = read(csv_tempfile)
    assert data == data_read


def test_write_h5(hdf5_tempfile):
    data = [
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\n", "3"],
    ]
    with pytest.raises(NotImplementedError):
        write(hdf5_tempfile, data)


def test_write_csv_params(csv_tempfile):
    data = [
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\n", "3"],
    ]
    write(csv_tempfile, data, delimiter=",", quotechar='"')
    data_read = read(csv_tempfile, delimiter=",", quotechar='"')
    assert data == data_read


def test_read_hdf5():
    path = "files/example.hdf5"
    source = pkg_resources.resource_filename(__name__, path)
    with pytest.raises(NotImplementedError):
        read(source)


def test_read_json():
    path = "files/example.json"
    source = pkg_resources.resource_filename(__name__, path)
    data_real = read(source)

    data_exp = {
        "a list": [1, 42, 3.141, 1337, "help", "€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    assert data_real == data_exp


def test_read_jsonl():
    path = "files/example.jsonl"
    source = pkg_resources.resource_filename(__name__, path)
    data_real = read(source)
    data_exp = [
        {"some": "thing"},
        {"foo": 17, "bar": False, "quux": True},
        {"may": {"include": "nested", "objects": ["and", "arrays"]}},
    ]
    assert len(data_real) == len(data_exp)
    for real, exp_ in zip(data_real, data_exp):
        assert real == exp_


def test_read_pickle():
    path = "files/example.pickle"
    source = pkg_resources.resource_filename(__name__, path)
    data_real = read(source)

    data_exp = {
        "a list": [1, 42, 3.141, 1337, "help", "€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    assert data_real == data_exp


def test_write_json(json_tempfile):
    data = {
        "a list": [1, 42, 3.141, 1337, "help", "€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(json_tempfile, data)
    data_read = read(json_tempfile)
    assert data == data_read


def test_write_jsonl(jsonl_tempfile):
    data = [
        {"some": "thing"},
        {"foo": 17, "bar": False, "quux": True},
        {"may": {"include": "nested", "objects": ["and", "arrays"]}},
    ]
    write(jsonl_tempfile, data)
    data_read = read(jsonl_tempfile)
    assert data == data_read


def test_write_jsonl_all_params(jsonl_tempfile):
    data = [
        {"some": "thing"},
        {"foo": 17, "bar": False, "quux": True},
        {"may": {"include": "nested", "objects": ["and", "arrays"]}},
    ]
    _write_jsonl(
        jsonl_tempfile,
        data,
        kwargs={"sort_keys": True, "separators": (",", ": "), "ensure_ascii": True},
    )
    data_read = read(jsonl_tempfile)
    assert data == data_read


def test_write_json_params(json_tempfile):
    data = {
        "a list": [1, 42, 3.141, 1337, "help", "€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(
        json_tempfile,
        data,
        indent=4,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    data_read = read(json_tempfile)
    assert data == data_read


def test_write_pickle(pickle_tempfile):
    data = {
        "a list": [1, 42, 3.141, 1337, "help", "€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(pickle_tempfile, data)
    data_read = read(pickle_tempfile)
    assert data == data_read


def test_write_pickle_protocol(pickle_tempfile):
    data = {
        "a list": [1, 42, 3.141, 1337, "help", "€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(pickle_tempfile, data, protocol=0)
    data_read = read(pickle_tempfile)
    assert data == data_read


def test_read_h5():
    source = pkg_resources.resource_filename("mpu", "io.py")
    with pytest.raises(NotImplementedError):
        read(source)


def test_gzip(pickle_tempfile):
    path = "files/example.csv"
    source = pkg_resources.resource_filename(__name__, path)
    gzip_file(source, pickle_tempfile)


def test_hash():
    path = "files/example.pickle"
    source = pkg_resources.resource_filename(__name__, path)
    assert mpu.io.hash(source) == "e845794fde22e7a33dd389ed0f5381ae042154c1"
    expected_hash_md5 = "c59db499d09531a5937c2ae2342cb18b"
    assert mpu.io.hash(source, method="md5") == expected_hash_md5


def test_get_creation_datetime():
    ret_val = mpu.io.get_creation_datetime(__file__)
    assert isinstance(ret_val, (type(None), datetime.datetime))


def test_get_creation_datetime_windows():
    with mock.patch("platform.system", mock.MagicMock(return_value="Windows")):
        ret_val = mpu.io.get_creation_datetime(__file__)
    assert isinstance(ret_val, (type(None), datetime.datetime))


def test_get_modification_datetime():
    ret_val = mpu.io.get_modification_datetime(__file__)
    assert isinstance(ret_val, datetime.datetime)


def test_get_access_datetime():
    ret_val = mpu.io.get_access_datetime(__file__)
    assert isinstance(ret_val, datetime.datetime)
