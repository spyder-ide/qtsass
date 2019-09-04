# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Contains the Qt implementation of the Watcher api."""

# yapf: disable

from __future__ import absolute_import

# Third party imports
QT_BINDING = None
if not QT_BINDING:
    try:
        from PySide2.QtWidgets import QApplication
        from PySide2.QtCore import QFileSystemWatcher
        QT_BINDING = 'pyside2'
    except ImportError:
        pass
if not QT_BINDING:
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QFileSystemWatcher
        QT_BINDING = 'pyqt5'
    except ImportError:
        pass
if not QT_BINDING:
    try:
        from PySide.QtGui import QApplication
        from PySide.QtCore import QFileSystemWatcher
        QT_BINDING == 'pyside'
    except ImportError:
        pass
if not QT_BINDING:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QFileSystemWatcher
    QT_BINDING == 'pyqt4'

# Local imports
from qtsass.watchers.api import Watcher

# yapf: enable


# TODO: This doesn't work yet.


class QtWatcher(Watcher):
    """The Qt implementation of the Watcher api. Uses a QFileSystemWatcher
    to monitor the filesystem.
    """
    _qt_binding = QT_BINDING

    def setup(self):
        self._qapp = QApplication.instance()
        if not self._qapp:
            raise RuntimeError('QtWatcher created before QApplication.')

        self._qfswatcher = QFileSystemWatcher()

    def connect(self, fn):
        self._qfswatcher.fileChanged.connect(fn)
        self._qfswatcher.directoryChanged.connect(fn)

    def disconnect(self, fn):
        self._qfswatcher.fileChanged.disconnect(fn)
        self._qfswatcher.directoryChanged.disconnect(fn)

    def start(self):
        self._qfswatcher.addPath(self._watch_dir)

    def stop(self):
        self._qfswatcher.removePath(self._watch_dir)
        self._qfswatcher = None

    def join(self):
        """Nothing to join here. Unlike PollingWatcher and WatchdogWatcher."""
