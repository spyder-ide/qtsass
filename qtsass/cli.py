#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""qtsass command line interface."""

# Standard library imports
from __future__ import absolute_import, print_function
import argparse
import os
import sys
import time
import logging
import signal

# Local imports
from qtsass.api import compile, compile_filename, compile_dirname, watch


logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)


def create_parser():
    """Create qtsass's cli parser."""

    parser = argparse.ArgumentParser(
        prog='QtSASS',
        description='Compile a Qt compliant CSS file from a SASS stylesheet.',
    )
    parser.add_argument('input', type=str, help='The SASS stylesheet file.')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='The path of the generated Qt compliant CSS file.'
    )
    parser.add_argument(
        '-w',
        '--watch',
        action='store_true',
        help='If set, recompile when the source file changes.'
    )
    return parser


def main():
    """qtsass's cli entry point."""

    args = create_parser().parse_args()
    file_mode = os.path.isfile(args.input)
    dir_mode = os.path.isdir(args.input)

    if file_mode and not args.output:

        with open(args.input, 'r') as f:
            string = f.read()

        css = compile(
            string,
            include_paths=os.path.abspath(os.path.dirname(args.input))
        )
        print(css)
        sys.exit(0)

    elif file_mode:
        compile_filename(args.input, args.output)

    elif dir_mode and not args.output:
        print('Error: missing required option: -o/--output')
        sys.exit(1)

    elif dir_mode:
        compile_dirname(args.input, args.output)

    else:
        print('Error: input must be a file or a directory')
        sys.exit(1)

    if args.watch:
        _log.info('qtsass is watching {}...'.format(args.input))
        observer = watch(args.input, args.output)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        sys.exit(0)
