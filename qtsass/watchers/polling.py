# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Contains the fallback implementation of the Watcher api."""

# yapf: disable

from __future__ import absolute_import, print_function

# Standard library imports
import atexit
import threading

# Local imports
from qtsass.watchers import snapshots
from qtsass.watchers.api import Watcher


# yapf: enable


class PollingThread(threading.Thread):
    """A thread that fires a callback at an interval."""

    def __init__(self, callback, interval):
        """Initialize the thread.

        :param callback: Callback function to repeat.
        :param interval: Number of seconds to sleep between calls.
        """
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
        """Check if the thread has started."""
        return self._started.is_set()

    @property
    def stopped(self):
        """Check if the thread has stopped."""
        return self._stopped.is_set()

    @property
    def shutdown(self):
        """Check if the thread has shutdown."""
        return self._shutdown.is_set()

    def stop(self):
        """Set the shutdown event for this thread and wait for it to stop."""
        if not self.started and not self.shutdown:
            return

        self._shutdown.set()
        self._stopped.wait()

    def run(self):
        """Threads main loop."""
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
        """Set up the PollingWatcher.

        A PollingThread is created but not started.
        """
        self._snapshot_depth = 2
        self._snapshot = snapshots.take(self._watch_dir, self._snapshot_depth)
        self._thread = PollingThread(self.run, interval=1)

    def start(self):
        """Start the PollingThread."""
        self._thread.start()

    def stop(self):
        """Stop the PollingThread."""
        self._thread.stop()

    def join(self):
        """Wait for the PollingThread to finish.

        You should always call stop before join.
        """
        self._thread.join()

    def run(self):
        """Take a new snapshot and call on_change when a change is detected.

        Called repeatedly by the PollingThread.
        """
        next_snapshot = snapshots.take(self._watch_dir, self._snapshot_depth)
        changes = snapshots.diff(self._snapshot, next_snapshot)
        if changes:
            self._snapshot = next_snapshot
            self.on_change()
