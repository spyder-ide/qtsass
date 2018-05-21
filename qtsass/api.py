# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""qtsass - Compile SCSS files to valid Qt stylesheets."""

# Standard library imports
from __future__ import absolute_import, print_function
import logging
import os

# Third party imports
import sass
from watchdog.observers import Observer

# Local imports
from qtsass.conformers import scss_conform, qt_conform
from qtsass.functions import qlineargradient, rgba
from qtsass.importers import qss_importer
from qtsass.events import SourceEventHandler


logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)


def compile(input_file):
    """Compile QtSASS to CSS."""

    _log.debug('Compiling {}...'.format(input_file))

    with open(input_file, 'r') as f:
        input_str = f.read()

    try:
        importer_root = os.path.dirname(os.path.abspath(input_file))
        return qt_conform(
            sass.compile(
                string=scss_conform(input_str),
                source_comments=False,
                custom_functions={
                    'qlineargradient': qlineargradient,
                    'rgba': rgba
                },
                importers=[(0, qss_importer(importer_root))]
            )
        )
    except sass.CompileError as e:
        _log.error('Failed to compile {}:\n{}'.format(input_file, e))
    return ""


def compile_filename(input_file, dest_file):
    """Compile QtSASS to CSS and save."""

    css = compile(input_file)
    with open(dest_file, 'w') as css_file:
        css_file.write(css)
        _log.info('Created CSS file {}'.format(dest_file))


def compile_dirname(input_dir, output_dir):
    """Compiles QtSASS files in a directory including subdirectories."""

    def is_valid(file):
        return not file.startswith('_') and file.endswith('.scss')

    for root, subdirs, files in os.walk(input_dir):
        relative_root = os.path.relpath(root, input_dir)
        output_root = os.path.join(output_dir, relative_root)

        for file in [f for f in files if is_valid(f)]:
            scss_path = os.path.join(root, file)
            css_file = os.path.splitext(file)[0] + '.css'
            css_path = os.path.join(output_root, css_file)
            if not os.path.isdir(output_root):
                os.makedirs(output_root)
            compile_filename(scss_path, css_path)


def watch(source, destination, compiler=None, recursive=True):
    """
    Watches a source file or directory, compiling QtSass files when modified.

    The compiler function defaults to compile_filename when source is a file
    and compile_dirname when source is a directory.

    :param source: Path to source QtSass file or directory.
    :param destination: Path to output css file or directory.
    :param compiler: Compile function (optional)
    :param recursive: If True, watch subdirectories (default: True).
    :returns: watchdog.Observer
    """

    if os.path.isfile(source):
        watch_dir = os.path.dirname(source)
        compiler = compiler or compile_filename
    else:
        watch_dir = source
        compiler = compiler or compile_dirname

    event_handler = SourceEventHandler(source, destination, compiler)

    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=recursive)
    return observer
