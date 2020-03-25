#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the mpu.io module."""

# Core Library
import datetime
import os
from tempfile import mkstemp

# Third party
import pkg_resources
import pytest

# First party
import mpu.io
from mpu.io import _write_jsonl, download, read, urlread, write


def test_download_with_path():
    source = (
        "https://upload.wikimedia.org/wikipedia/commons/e/e9/"
        "Aurelia-aurita-3-1-style.jpg"
    )
    _, sink = mkstemp(suffix="image.jpg")
    download(source, sink)
    assert os.path.getsize(sink) == 116087
    os.remove(sink)  # cleanup of mkstemp


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
        ["a", "b", "c"],
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\r\n", "3"],
        ["3.141", "Special char test: €üößł", "2.7"],
    ]
    assert len(data_real) == len(data_exp)
    assert data_real[0] == data_exp[0]
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
        {"a": "-2", "b": "an interstellar hitchhiker can have.\r\n", "c": "3"},
        {"a": "3.141", "b": "Special char test: €üößł", "c": "2.7"},
    ]
    assert len(data_real) == len(data_exp)
    assert data_real[0] == data_exp[0]
    assert data_real == data_exp


def test_write_csv():
    _, filepath = mkstemp(suffix=".csv", prefix="mpu_test")
    data = [
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\r\n", "3"],
    ]
    write(filepath, data)
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_write_h5():
    _, filepath = mkstemp(suffix=".hdf5", prefix="mpu_test")
    data = [
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\r\n", "3"],
    ]
    with pytest.raises(NotImplementedError):
        write(filepath, data)
    os.remove(filepath)  # cleanup of mkstemp


def test_write_csv_params():
    _, filepath = mkstemp(suffix=".csv", prefix="mpu_test")
    data = [
        ["1", "A towel,", "1.0"],
        ["42", " it says, ", "2.0"],
        ["1337", "is about the most ", "-1"],
        ["0", "massively useful thing ", "123"],
        ["-2", "an interstellar hitchhiker can have.\r\n", "3"],
    ]
    write(filepath, data, delimiter=",", quotechar='"')
    data_read = read(filepath, delimiter=",", quotechar='"')
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


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
        "a list": [1, 42, 3.141, 1337, "help", u"€"],
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
        "a list": [1, 42, 3.141, 1337, "help", u"€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    assert data_real == data_exp


def test_write_json():
    _, filepath = mkstemp(suffix=".json", prefix="mpu_test")
    data = {
        "a list": [1, 42, 3.141, 1337, "help", u"€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(filepath, data)
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_write_jsonl():
    _, filepath = mkstemp(suffix=".jsonl", prefix="mpu_test")
    data = [
        {"some": "thing"},
        {"foo": 17, "bar": False, "quux": True},
        {"may": {"include": "nested", "objects": ["and", "arrays"]}},
    ]
    write(filepath, data)
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_write_jsonl_all_params():
    _, filepath = mkstemp(suffix=".jsonl", prefix="mpu_test")
    data = [
        {"some": "thing"},
        {"foo": 17, "bar": False, "quux": True},
        {"may": {"include": "nested", "objects": ["and", "arrays"]}},
    ]
    _write_jsonl(
        filepath,
        data,
        kwargs={"sort_keys": True, "separators": (",", ": "), "ensure_ascii": True},
    )
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_write_json_params():
    _, filepath = mkstemp(suffix=".json", prefix="mpu_test")
    data = {
        "a list": [1, 42, 3.141, 1337, "help", u"€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(
        filepath,
        data,
        indent=4,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_write_pickle():
    _, filepath = mkstemp(suffix=".pickle", prefix="mpu_test")
    data = {
        "a list": [1, 42, 3.141, 1337, "help", u"€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(filepath, data)
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_write_pickle_protocol():
    _, filepath = mkstemp(suffix=".pickle", prefix="mpu_test")
    data = {
        "a list": [1, 42, 3.141, 1337, "help", u"€"],
        "a string": "bla",
        "another dict": {"foo": "bar", "key": "value", "the answer": 42},
    }
    write(filepath, data, protocol=0)
    data_read = read(filepath)
    assert data == data_read
    os.remove(filepath)  # cleanup of mkstemp


def test_read_h5():
    source = pkg_resources.resource_filename("mpu", "io.py")
    with pytest.raises(NotImplementedError):
        read(source)


def test_hash():
    path = "files/example.pickle"
    source = pkg_resources.resource_filename(__name__, path)
    assert mpu.io.hash(source) == "e845794fde22e7a33dd389ed0f5381ae042154c1"
    expected_hash_md5 = "c59db499d09531a5937c2ae2342cb18b"
    assert mpu.io.hash(source, method="md5") == expected_hash_md5


def test_get_creation_datetime():
    ret_val = mpu.io.get_creation_datetime(__file__)
    assert isinstance(ret_val, (type(None), datetime.datetime))


def test_get_modification_datetime():
    ret_val = mpu.io.get_modification_datetime(__file__)
    assert isinstance(ret_val, datetime.datetime)


def test_get_access_datetime():
    ret_val = mpu.io.get_access_datetime(__file__)
    assert isinstance(ret_val, datetime.datetime)
