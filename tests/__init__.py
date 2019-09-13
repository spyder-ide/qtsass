# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------

# Standard library imports
from os.path import dirname, join, normpath
import os
import time


PROJECT_DIR = normpath(dirname(dirname(__file__)))
EXAMPLES_DIR = normpath(join(PROJECT_DIR, 'examples'))


def example(*paths):
    """Get path to an example."""

    return normpath(join(dirname(__file__), '..', 'examples', *paths))


def touch(file):
    """Touch a file."""

    with open(str(file), 'a'):
        os.utime(str(file), None)


def await_condition(condition, timeout=20, qt_app=None):
    """Return True if a condition is met in the given timeout period"""

    for _ in range(timeout):
        if qt_app:
            # pump event loop while waiting for condition
            qt_app.processEvents()
        if condition():
            return True
        time.sleep(0.1)
    return False
