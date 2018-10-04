#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The _cli module is for providing the CLI of mpu.

Please do not import anything from it.
"""

import mpu.package


def main():
    """Command line interface of mpu."""
    parser = get_parser()
    args = parser.parse_args()
    if hasattr(args, 'func') and args.func:
        args.func(args)
    else:
        parser.print_help()


def get_parser():
    """Get parser for mpu."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version',
                        action='version',
                        version='mpu {}'.format(mpu.__version__))
    subparsers = parser.add_subparsers(help='Python package commands')
    package_parser = subparsers.add_parser('package')
    mpu.package.cli.get_parser(package_parser)
    return parser
