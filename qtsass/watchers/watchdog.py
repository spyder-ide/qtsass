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
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Local imports
from qtsass.watchers.api import Watcher

# yapf: enable


class SourceChangedEventHandler(FileSystemEventHandler):
    """Source event hanlder."""

    def __init__(self, compile, callbacks):
        """Source event hanlder."""
        super(SourceChangedEventHandler, self).__init__()
        self._compile = compile
        self._callbacks = callbacks

    def on_modified(self, event):
        """Override watchdog method to handle on file modification events."""
        css = self._compile()
        for callback in self._callbacks:
            callback(css)


class WatchdogWatcher(Watcher):
    """Watches a file or directory for changes and calls the provided compiler
    whenever a change is detected.
    """

    def setup(self):
        self._callbacks = set()
        self._handler = SourceChangedEventHandler(
            self.compile,
            self._callbacks
        )
        self._observer = Observer()
        self._observer.schedule(self._handler, self._watch_dir, recursive=True)

    def connect(self, fn):
        self._callbacks.add(fn)

    def disconnect(self, fn):
        self._callbacks.discard(fn)

    def start(self):
        self._observer.start()

    def stop(self):
        self._observer.stop()

    def join(self):
        self._observer.join()
