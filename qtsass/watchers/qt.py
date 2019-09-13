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

# Local imports
from qtsass.watchers.polling import PollingWatcher


# We cascade through Qt bindings here rather than relying on a comprehensive
# Qt compatability library like qtpy or Qt.py. This prevents us from forcing a
# specific compatability library on users.
QT_BINDING = None
if not QT_BINDING:
    try:
        from PySide2.QtWidgets import QApplication
        from PySide2.QtCore import QObject, Signal
        QT_BINDING = 'pyside2'
    except ImportError:
        pass
if not QT_BINDING:
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QObject
        from PyQt5.QtCore import pyqtSignal as Signal
        QT_BINDING = 'pyqt5'
    except ImportError:
        pass
if not QT_BINDING:
    try:
        from PySide.QtGui import QApplication
        from PySide2.QtCore import QObject, Signal
        QT_BINDING == 'pyside'
    except ImportError:
        pass
if not QT_BINDING:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QObject
    from PyQt4.QtCore import pyqtSignal as Signal
    QT_BINDING == 'pyqt4'


# yapf: enable


class QtDispatcher(QObject):
    """Used by QtWatcher to dispatch callbacks in the main ui thread."""

    signal = Signal()


class QtWatcher(PollingWatcher):
    """The Qt implementation of the Watcher api.

    Subclasses PollingWatcher but dispatches :meth:`compile_and_dispatch`
    using a Qt Signal to ensure that these calls are executed in the main ui
    thread. We aren't using a QFileSystemWatcher because it fails to report
    changes in certain circumstances.
    """

    _qt_binding = QT_BINDING

    def setup(self):
        """Set up QtWatcher."""
        super(QtWatcher, self).setup()
        self._qtdispatcher = None

    @property
    def qtdispatcher(self):
        """Get the QtDispatcher."""
        if self._qtdispatcher is None:
            self._qtdispatcher = QtDispatcher()
            self._qtdispatcher.signal.connect(self.compile_and_dispatch)
        return self._qtdispatcher

    def on_change(self):
        """Call when a change is detected."""
        self._log.debug('Change detected...')

        # If a QApplication event loop has not been started
        # call compile_and_dispatch in the current thread.
        if not QApplication.instance():
            return super(PollingWatcher, self).compile_and_dispatch()

        # Create and use a QtDispatcher to ensure compile and any
        # connected callbacks get executed in the main gui thread.
        self.qtdispatcher.signal.emit()
