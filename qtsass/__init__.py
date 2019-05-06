# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------

# yapf: disable

from __future__ import absolute_import

# Local imports
from qtsass.api import compile, compile_dirname, compile_filename, watch


# yapf: enable

# Constants
VERSION_INFO = (0, 1, 2, 'dev0')
__version__ = '.'.join(map(str, VERSION_INFO))
