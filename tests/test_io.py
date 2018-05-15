#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
from tempfile import mkstemp
import os
import pkg_resources
import unittest

# internal modules
from mpu.io import (download, read, write)


class IoTest(unittest.TestCase):

    def test_download_with_path(self):
        source = 'http://www.martin-thoma.de/bilder/Martin_Thoma_web_thumb.jpg'
        fd, sink = mkstemp(suffix='image.jpg')
        download(source, sink)
        os.remove(sink)  # cleanup of mkstemp

    def test_download_without_path(self):
        source = 'http://www.martin-thoma.de/bilder/Martin_Thoma_web_thumb.jpg'
        sink = download(source)
        os.remove(sink)  # cleanup of mkstemp

    def test_read_csv(self):
        path = '../tests/files/example.csv'
        source = pkg_resources.resource_filename('mpu', path)
        data_real = read(source)
        data_exp = [['1', "A towel,", '1.0'],
                    ['42', " it says, ", '2.0'],
                    ['1337', "is about the most ", '-1'],
                    ['0', "massively useful thing ", '123'],
                    ['-2', "an interstellar hitchhiker can have.", '3'],
                    ['3.141', "Special char test: €üößł", '2.7']]
        self.assertEquals(len(data_real), len(data_exp))
        self.assertEquals(data_real[0], data_exp[0])
        self.assertEquals(data_real, data_exp)
        data_real = read(source, skiprows=1)
        self.assertEquals(data_real, data_exp[1:])
        data_real = read(source, skiprows=1, delimiter=',', quotechar='"')
        self.assertEquals(data_real, data_exp[1:])

    def test_write_csv(self):
        handle, filepath = mkstemp(suffix='.csv', prefix='mpu_test')
        data = [['1', "A towel,", '1.0'],
                ['42', " it says, ", '2.0'],
                ['1337', "is about the most ", '-1'],
                ['0', "massively useful thing ", '123'],
                ['-2', "an interstellar hitchhiker can have.", '3']]
        write(filepath, data)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_read_hdf5(self):
        path = '../tests/files/example.hdf5'
        source = pkg_resources.resource_filename('mpu', path)
        with self.assertRaises(Exception):
            read(source)

    def test_read_json(self):
        path = '../tests/files/example.json'
        source = pkg_resources.resource_filename('mpu', path)
        data_real = read(source)

        data_exp = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                    'a string': 'bla',
                    'another dict': {'foo': 'bar',
                                     'key': 'value',
                                     'the answer': 42}}
        self.assertEquals(data_real, data_exp)

    def test_write_json(self):
        handle, filepath = mkstemp(suffix='.json', prefix='mpu_test')
        data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                'a string': 'bla',
                'another dict': {'foo': 'bar',
                                 'key': 'value',
                                 'the answer': 42}}
        write(filepath, data)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_read_h5(self):
        source = pkg_resources.resource_filename('mpu', 'io.py')
        with self.assertRaises(Exception):
            read(source)
