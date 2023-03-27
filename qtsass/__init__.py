# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""
The SASS language brings countless amazing features to CSS.

Besides being used in web development, CSS is also the way to stylize Qt-based
desktop applications. However, Qt's CSS has a few variations that prevent the
direct use of SASS compiler.

The purpose of qtsass is to fill the gap between SASS and Qt-CSS by handling
those variations.
"""

# yapf: disable

from __future__ import absolute_import

# Standard library imports
import logging

# Local imports
from qtsass.api import (
    compile,
    compile_dirname,
    compile_filename,
    enable_logging,
    watch,
)


# yapf: enable

# Setup Logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
enable_logging()

# Constants
__version__ = '0.4.0'


def _to_version_info(version):
    """Convert a version string to a number and string tuple."""
    parts = []
    for part in version.split('.'):
        try:
            part = int(part)
        except ValueError:
            pass

        parts.append(part)

    return tuple(parts)


VERSION_INFO = _to_version_info(__version__)
