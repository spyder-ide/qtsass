# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""The qtsass Watcher is responsible for watching and recompiling sass.

The default Watcher is the QtWatcher. If Qt is unavailable we fallback to the
PollingWatcher.
"""

# yapf: disable

from __future__ import absolute_import

# Local imports
from qtsass.watchers.polling import PollingWatcher


try:
    from qtsass.watchers.qt import QtWatcher
except ImportError:
    QtWatcher = None


# yapf: enable

Watcher = QtWatcher or PollingWatcher
