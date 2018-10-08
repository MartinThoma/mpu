#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Machine Learning functions."""

# core modules
from pkg_resources import resource_filename
from shutil import copyfile
import os
import re

# internal modules
from mpu.shell import text_input


def run_init(args):
    """
    Run project initialization.

    This will ask the user for input.

    Parameters
    ----------
    args : argparse named arguments
    """
    root = args.root
    if root is None:
        root = '.'
    root = os.path.abspath(root)

    project_data = _get_package_data()
    project_name = project_data['project_name']

    directories = [os.path.join(root, 'bin'),
                   os.path.join(root, 'docs'),
                   os.path.join(root, 'tests'),
                   os.path.join(root, project_name),
                   ]
    for dir_path in directories:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    script_paths = [os.path.join(root, 'README.md'),
                    os.path.join(root, 'tests/__init__.py'),
                    ]
    for script_path in script_paths:
        if not os.path.exists(script_path):
            os.mknod(script_path)

    copy_samples = [(resource_filename('mpu', 'package/templates/tox.ini.txt'),
                     os.path.join(root, 'tox.ini')),
                    (resource_filename('mpu',
                                       'package/templates/setup.cfg.txt'),
                     os.path.join(root, 'setup.cfg')),
                    (resource_filename('mpu',
                                       'package/templates/setup.py.txt'),
                     os.path.join(root, 'setup.py')),
                    (resource_filename('mpu',
                                       'package/templates/_version.py.txt'),
                     os.path.join(root, project_name + '/_version.py')),
                    (resource_filename('mpu',
                                       'package/templates/coveragerc.txt'),
                     os.path.join(root, '.coveragerc')),
                    (resource_filename('mpu', 'package/templates/init.py.txt'),
                     os.path.join(root, project_name + '/__init__.py')),
                    ]
    translate = {'[[project_name]]': project_data['project_name'],
                 '[[license]]': project_data['license'],
                 '[[author]]': project_data['author'],
                 '[[email]]': project_data['email'],
                 }
    for source, destination in copy_samples:
        if not os.path.exists(destination):
            copyfile(source, destination)
            _adjust_template(destination, translate)


def _get_package_data():
    project_data = {}
    project_data['project_name'] = text_input('Python package name: ')
    project_data['license'] = (text_input('License [default: MIT]: ') or
                               'MIT')
    project_data['author'] = text_input('Author: ')
    project_data['email'] = text_input('E-mail: ')
    return project_data


def _multiple_replace(text, search_replace_dict):
    """
    Replace multiple things at once in a text.

    Parameters
    ----------
    text : str
    search_replace_dict : dict

    Returns
    -------
    replaced_text : str

    Examples
    --------
    >>> d = {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e'}
    >>> _multiple_replace('abcdefghijklm', d)
    'bcdeefghijklm'
    """
    # Create a regular expression from all of the dictionary keys
    regex = re.compile("|".join(map(re.escape, search_replace_dict.keys())))

    # For each match, look up the corresponding value in the dictionary
    return regex.sub(lambda match: search_replace_dict[match.group(0)], text)


def _adjust_template(filepath, translate):
    """
    Search and replace contents of a filepath.

    Parameters
    ----------
    filepath : str
    translate : dict
    """
    with open(filepath, 'r') as file:
        filedata = file.read()

    filedata = _multiple_replace(filedata, translate)

    with open(filepath, 'w') as file:
        file.write(filedata)


def get_parser(parser=None):
    """Get parser for mpu."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    if parser is None:
        parser = ArgumentParser(description=__doc__,
                                formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()
    pkg_init_parser = subparsers.add_parser('init')
    pkg_init_parser.add_argument("root",
                                 nargs='?',
                                 help="project root - should be empty")
    pkg_init_parser.set_defaults(func=run_init)
    return parser
