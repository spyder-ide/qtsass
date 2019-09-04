# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""qtsass.watchers.api - FS Watcher api."""

# yapf: disable

from __future__ import absolute_import

# yapf: enable


class Watcher(object):
    """Watches a file or directory for changes and calls the provided compiler
    whenever a change is detected.
    """

    def __init__(self, watch_dir, source, destination, compiler):
        self._watch_dir = watch_dir
        self._source = source
        self._destination = destination
        self._compiler = compiler
        self.setup()

    def compile(self):
        print('Watcher.compile - %s > %s' % (self._source, self._destination))
        return self._compiler(self._source, self._destination)

    def setup(self):
        """Perform any setup required by this Watcher."""
        return NotImplemented

    def connect(self, fn):
        """Connect a handler to be called when this Watcher detects a
        file or directory change. Called after setup to connect compile to
        as a handler."""
        return NotImplemented

    def disconnect(self, fn):
        """Disconnect a handler from this Watcher."""
        return NotImplemented

    def start(self):
        """Start this Watcher."""
        return NotImplemented

    def stop(self):
        """Stop this Watcher."""
        return NotImplemented

    def join(self):
        """Wait for this Watcher to finish."""
        return NotImplemented
