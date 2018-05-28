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
        source = ('https://upload.wikimedia.org/wikipedia/commons/e/e9/'
                  'Aurelia-aurita-3-1-style.jpg')
        _, sink = mkstemp(suffix='image.jpg')
        download(source, sink)
        self.assertEquals(os.path.getsize(sink), 116087)
        os.remove(sink)  # cleanup of mkstemp

    def test_download_without_path(self):
        source = ('https://upload.wikimedia.org/wikipedia/commons/e/e9/'
                  'Aurelia-aurita-3-1-style.jpg')
        sink = download(source)
        download(source, sink)
        self.assertEquals(os.path.getsize(sink), 116087)
        os.remove(sink)  # cleanup of mkstemp

    def test_read_csv(self):
        path = '../tests/files/example.csv'
        source = pkg_resources.resource_filename('mpu', path)
        data_real = read(source)
        data_exp = [['a', 'b', 'c'],
                    ['1', "A towel,", '1.0'],
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

    def test_read_csv_dicts(self):
        path = '../tests/files/example.csv'
        source = pkg_resources.resource_filename('mpu', path)
        data_real = read(source, format='dicts')
        data_exp = [{'a': '1', 'b': "A towel,", 'c': '1.0'},
                    {'a': '42', 'b': " it says, ", 'c': '2.0'},
                    {'a': '1337', 'b': "is about the most ", 'c': '-1'},
                    {'a': '0', 'b': "massively useful thing ", 'c': '123'},
                    {'a': '-2', 'b': "an interstellar hitchhiker can have.",
                     'c': '3'},
                    {'a': '3.141', 'b': "Special char test: €üößł", 'c': '2.7'}
                    ]
        self.assertEquals(len(data_real), len(data_exp))
        self.assertEquals(data_real[0], data_exp[0])
        self.assertEquals(data_real, data_exp)

    def test_write_csv(self):
        _, filepath = mkstemp(suffix='.csv', prefix='mpu_test')
        data = [['1', "A towel,", '1.0'],
                ['42', " it says, ", '2.0'],
                ['1337', "is about the most ", '-1'],
                ['0', "massively useful thing ", '123'],
                ['-2', "an interstellar hitchhiker can have.", '3']]
        write(filepath, data)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_write_csv_params(self):
        _, filepath = mkstemp(suffix='.csv', prefix='mpu_test')
        data = [['1', "A towel,", '1.0'],
                ['42', " it says, ", '2.0'],
                ['1337', "is about the most ", '-1'],
                ['0', "massively useful thing ", '123'],
                ['-2', "an interstellar hitchhiker can have.", '3']]
        write(filepath, data, delimiter=',', quotechar='"')
        data_read = read(filepath, delimiter=',', quotechar='"')
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

    def test_read_pickle(self):
        path = '../tests/files/example.pickle'
        source = pkg_resources.resource_filename('mpu', path)
        data_real = read(source)

        data_exp = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                    'a string': 'bla',
                    'another dict': {'foo': 'bar',
                                     'key': 'value',
                                     'the answer': 42}}
        self.assertEquals(data_real, data_exp)

    def test_write_json(self):
        _, filepath = mkstemp(suffix='.json', prefix='mpu_test')
        data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                'a string': 'bla',
                'another dict': {'foo': 'bar',
                                 'key': 'value',
                                 'the answer': 42}}
        write(filepath, data)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_write_json_params(self):
        _, filepath = mkstemp(suffix='.json', prefix='mpu_test')
        data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                'a string': 'bla',
                'another dict': {'foo': 'bar',
                                 'key': 'value',
                                 'the answer': 42}}
        write(filepath, data,
              indent=4,
              sort_keys=True,
              separators=(',', ':'),
              ensure_ascii=False)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_write_pickle(self):
        _, filepath = mkstemp(suffix='.pickle', prefix='mpu_test')
        data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                'a string': 'bla',
                'another dict': {'foo': 'bar',
                                 'key': 'value',
                                 'the answer': 42}}
        write(filepath, data)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_write_pickle_protocol(self):
        _, filepath = mkstemp(suffix='.pickle', prefix='mpu_test')
        data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
                'a string': 'bla',
                'another dict': {'foo': 'bar',
                                 'key': 'value',
                                 'the answer': 42}}
        write(filepath, data, protocol=0)
        data_read = read(filepath)
        self.assertEquals(data, data_read)
        os.remove(filepath)  # cleanup of mkstemp

    def test_read_h5(self):
        source = pkg_resources.resource_filename('mpu', 'io.py')
        with self.assertRaises(Exception):
            read(source)
