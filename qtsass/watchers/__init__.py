# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""The qtsass Watcher is responsible for watching and recompiling sass when
it changes on the filesystem. Here we choose a Watcher implementation based on
the availability.

Qt and watchdog implementations are provided. A RuntimeError is raised if no
implementation can be imported.
"""

# yapf: disable

from __future__ import absolute_import

# Local imports
from qtsass.watchers.polling import PollingWatcher

try:
    from qtsass.watchers.qt import QtWatcher
except ImportError:
    QtWatcher = None

try:
    from qtsass.watchers.watchdog import WatchdogWatcher
except ImportError:
    WatchdogWatcher = None

# yapf: enable

Watcher = QtWatcher or WatchdogWatcher or PollingWatcher
