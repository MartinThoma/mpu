#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
from setuptools import find_packages
from setuptools import setup
import io
import os
import unittest

# internal modules
exec(open('mpu/_version.py').read())


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()


def my_test_suite():
    """Return a a composite test consisting of a number of TestCases."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


requires_datetime = ['pytz']
requires_image = ['Pillow']
requires_io = ['pytz', 'tzlocal']
requires_aws = ['boto3']
requires_tests = ['pytest', 'pytest-cov', 'pytest-mccabe', 'pytest-flake8',
                  'simplejson']
requires_all = (['pandas', 'python-magic'] + requires_datetime +
                requires_image + requires_io + requires_aws + requires_tests)

config = {
    'name': 'mpu',
    'version': __version__,  # noqa
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'package_data': {'mpu': ['units/currencies.csv',
                             'data/*',
                             'package/templates/*']},
    'extras_require': {'all': requires_all,
                       'aws': requires_aws,
                       'datetime': requires_datetime,
                       'image': requires_image,
                       'io': requires_io,
                       'tests': requires_tests},
    'tests_require': requires_tests,
    'entry_points': {
        'console_scripts': ['mpu=mpu._cli:main']
    },
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/mpu',
    'license': 'MIT',
    'description': 'Martins Python Utilities',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'install_requires': [],
    'keywords': ['utility'],
    'download_url': 'https://github.com/MartinThoma/mpu',
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3.6',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': True,
    'test_suite': 'setup.my_test_suite',
}

setup(**config)
