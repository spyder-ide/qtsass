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

from __future__ import absolute_import, print_function

# Standard library imports
import atexit
import os
import time
import threading

# Local imports
from qtsass.watchers.api import Watcher
from qtsass.importers import norm_path


class PollingThread(threading.Thread):
    """A daemon thread that continually fires a callback at the specified
    interval."""

    def __init__(self, callback, interval):
        super(PollingThread, self).__init__()
        self.daemon = True

        self.callback = callback
        self.interval = interval
        self._shutdown = threading.Event()
        self._stopped = threading.Event()
        self._started = threading.Event()
        atexit.register(self.stop)

    @property
    def started(self):
        return self._started.is_set()

    @property
    def stopped(self):
        return self._stopped.is_set()

    @property
    def shutdown(self):
        return self._shutdown.is_set()

    def stop(self):
        if not self.started and not self.shutdown:
            return

        self._shutdown.set()
        self._stopped.wait()

    def run(self):
        try:
            self._started.set()

            while True:
                self.callback()
                if self._shutdown.wait(self.interval):
                    break

        finally:
            self._stopped.set()


class PollingWatcher(Watcher):
    """Polls a directory recursively for changes.

    Detects file and directory changes, deletions, and creations. Recursion
    depth is limited to 2 levels. We use a limit because the scss file we're
    watching for changes could be sitting in the root of a project rather than
    a dedicated scss directory. That could lead to snapshots taking too long
    to build and diff. It's probably safe to assume that users aren't nesting
    scss deeper than a couple of levels.
    """

    def setup(self):
        self._snapshot_depth = 2
        self._snapshot = self._take_snapshot()
        self._callbacks = set()
        self._stop = False
        self._thread = PollingThread(self._check_snapshot, interval=1)

    def connect(self, fn):
        self._callbacks.add(fn)

    def disconnect(self, fn):
        self._callbacks.discard(fn)

    def start(self):
        self._thread.start()

    def stop(self):
        self._thread.stop()

    def join(self):
        self._thread.join()

    def _take_snapshot(self):
        snapshot = {}
        base_depth = len(norm_path(self._watch_dir).split('/'))

        for root, _, files in os.walk(self._watch_dir):

            path = norm_path(root)
            if len(path.split('/')) - base_depth > self._snapshot_depth:
                break

            snapshot[path] = os.path.getmtime(path)
            for f in files:
                path = norm_path(root, f)
                snapshot[path] = os.path.getmtime(path)

        return snapshot

    def _diff_snapshots(self, prev_snapshot, next_snapshot):
        changes = {}
        for path in set(prev_snapshot.keys()) | set(next_snapshot.keys()):
            if path in prev_snapshot and path not in next_snapshot:
                changes[path] = 'Deleted'
            elif path not in prev_snapshot and path in next_snapshot:
                changes[path] = 'Created'
            else:
                prev_mtime = prev_snapshot[path]
                next_mtime = next_snapshot[path]
                if next_mtime > prev_mtime:
                    changes[path] = 'Changed'
        return changes

    def _check_snapshot(self):
        next_snapshot = self._take_snapshot()
        changes = self._diff_snapshots(self._snapshot, next_snapshot)
        if changes:
            self._snapshot = next_snapshot
            self._dispatch()

    def _dispatch(self):
        css = self.compile()
        for callback in self._callbacks:
            callback(css)
