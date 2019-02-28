# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------

# Standard library imports
import os
import time
from os.path import normpath, join, dirname


PROJECT_DIR = normpath(dirname(dirname(__file__)))
EXAMPLES_DIR = normpath(join(PROJECT_DIR, 'examples'))


def example(*paths):
    """Get path to an example."""

    return normpath(join(dirname(__file__), '..', 'examples', *paths))


def touch(file):
    """Touch a file."""

    with open(file, 'a') as f:
        os.utime(file, None)


def await_condition(condition, timeout=2000):
    """Return True if a condition is met in the given timeout period"""

    for _ in range(timeout):
        if condition():
            return True
        time.sleep(0.001)
    return False


