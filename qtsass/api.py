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

# Local imports
from qtsass.conformers import scss_conform, qt_conform
from qtsass.functions import qlineargradient, rgba
from qtsass.importers import qss_importer


logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)


def compile(input_file):
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


def compile_and_save(input_file, dest_file):
    stylesheet = compile(input_file)
    if dest_file:
        with open(dest_file, 'w') as css_file:
            css_file.write(stylesheet)
            _log.info('Created CSS file {}'.format(dest_file))
    else:
        print(stylesheet)
