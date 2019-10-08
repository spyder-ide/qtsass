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

# yapf: disable

from __future__ import absolute_import, print_function

# Standard library imports
import argparse
import logging
import os
import sys
import time

# Local imports
from qtsass.api import (
    compile,
    compile_dirname,
    compile_filename,
    enable_logging,
    watch,
)


# yapf: enable

_log = logging.getLogger(__name__)


def create_parser():
    """Create qtsass's cli parser."""
    parser = argparse.ArgumentParser(
        prog='QtSASS',
        description='Compile a Qt compliant CSS file from a SASS stylesheet.',
    )
    parser.add_argument(
        'input',
        type=str,
        help='The SASS stylesheet file.',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='The path of the generated Qt compliant CSS file.',
    )
    parser.add_argument(
        '-w',
        '--watch',
        action='store_true',
        help='If set, recompile when the source file changes.',
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Set the logging level to DEBUG.',
    )
    return parser


def main():
    """CLI entry point."""
    args = create_parser().parse_args()

    # Setup CLI logging
    debug = os.environ.get('QTSASS_DEBUG', args.debug)
    if debug in ('1', 'true', 'True', 'TRUE', 'on', 'On', 'ON', True):
        level = logging.DEBUG
    else:
        level = logging.INFO
    enable_logging(level)

    # Add a StreamHandler
    handler = logging.StreamHandler()
    if level == logging.DEBUG:
        fmt = '%(levelname)-8s: %(name)s> %(message)s'
        handler.setFormatter(logging.Formatter(fmt))
    logging.root.addHandler(handler)
    logging.root.setLevel(level)

    file_mode = os.path.isfile(args.input)
    dir_mode = os.path.isdir(args.input)

    if file_mode and not args.output:
        with open(args.input, 'r') as f:
            string = f.read()

        css = compile(
            string,
            include_paths=os.path.abspath(os.path.dirname(args.input)),
        )
        print(css)
        sys.exit(0)

    elif file_mode:
        _log.debug('compile_filename({}, {})'.format(args.input, args.output))
        compile_filename(args.input, args.output)

    elif dir_mode and not args.output:
        print('Error: missing required option: -o/--output')
        sys.exit(1)

    elif dir_mode:
        _log.debug('compile_dirname({}, {})'.format(args.input, args.output))
        compile_dirname(args.input, args.output)

    else:
        print('Error: input must be a file or a directory')
        sys.exit(1)

    if args.watch:
        _log.info('qtsass is watching {}...'.format(args.input))

        watcher = watch(args.input, args.output)
        watcher.start()
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            watcher.stop()
        watcher.join()
        sys.exit(0)
