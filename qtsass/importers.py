# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Libsass importers."""

# Standard library imports
from __future__ import absolute_import
import os

# Local imports
from qtsass.conformers import scss_conform


def qss_importer(where):
    """
    Returns a function which conforms imported qss files to valid scss to be
    used as an importer for sass.compile.

    :param where: Directory containing scss, css, and sass files
    """

    def find_file(import_file):

        if os.path.isfile(import_file):
            return import_file
        extensions = ['.scss', '.css', '.sass']
        for ext in extensions:
            potential_file = import_file + ext
            if os.path.isfile(potential_file):
                return potential_file
            potential_file = os.path.join(where, import_file + ext)
            if os.path.isfile(potential_file):
                return potential_file
        return import_file

    def import_and_conform_file(import_file):

        real_import_file = find_file(import_file)
        with open(real_import_file, 'r') as f:
            import_str = f.read()

        return [(import_file, scss_conform(import_str))]

    return import_and_conform_file
