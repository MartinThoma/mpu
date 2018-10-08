#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
from pkg_resources import resource_filename
from shutil import copyfile
from tempfile import mkstemp, mkdtemp
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # Python 2.7
import os
import unittest
import shutil

# internal modules
import mpu.package.cli


class PackageTest(unittest.TestCase):

    def test_parser(self):
        mpu.package.cli.get_parser()

    @patch('mpu.package.cli.text_input', return_value='foobar')
    def test_get_package_data(self, input_patch):
        self.assertEqual(mpu.package.cli._get_package_data(),
                         {'project_name': 'foobar',
                          'license': 'foobar',
                          'author': 'foobar',
                          'email': 'foobar'})

    def test_adjust_template(self):
        _, sink = mkstemp(prefix='mpu_', suffix='init.py.txt')
        source = resource_filename('mpu', 'package/templates/init.py.txt')
        copyfile(source, sink)

        translate = {'[[project_name]]': 'foobar_project'}
        mpu.package.cli._adjust_template(sink, translate)

        expected = '''# -*- coding: utf-8 -*-

# internal modules
from foobar_project._version import __version__
'''
        with open(sink) as f:
            content = f.read()
        self.assertEqual(content, expected)
        os.remove(sink)  # cleanup of mkstemp

    @patch('mpu.package.cli.text_input', return_value='foobar')
    def test_cli_run_init(self, input_patch):
        class Object(object):
            pass
        args = Object()
        args.root = mkdtemp(prefix='mpu_')
        mpu.package.cli.run_init(args)
        if os.path.exists(args.root) and os.path.isdir(args.root):
            shutil.rmtree(args.root)
