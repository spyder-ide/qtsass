# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------

# Standard library imports
from __future__ import absolute_import

# Local imports
from qtsass.api import compile, compile_filename, compile_dirname, watch


VERSION_INFO = (0, 1, 1)
__version__ = '.'.join(map(str, VERSION_INFO))
