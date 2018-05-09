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
import time
import logging

# Third party imports
from watchdog.observers import Observer

# Local imports
from qtsass.api import compile_and_save
from qtsass.events import SourceModificationEventHandler


logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)


def main_parser():
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

    args = main_parser().parse_args()
    compile_and_save(args.input, args.output)

    if args.watch:
        watched_dir = os.path.abspath(os.path.dirname(args.input))
        event_handler = SourceModificationEventHandler(
            args.input,
            args.output,
            watched_dir,
            compile_and_save
        )
        _log.info('qtsass is watching {}...'.format(args.input))
        observer = Observer()
        observer.schedule(event_handler, watched_dir, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
