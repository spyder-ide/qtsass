# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""The filesystem watcher api."""

# yapf: disable

from __future__ import absolute_import
import logging


# yapf: enable


_log = logging.getLogger(__name__)


class Watcher(object):
    """Watcher base class.

    Watchers monitor a file or directory and call the on_change method when a
    change occurs. The on_change method should trigger the compiler function
    passed in during construction and dispatch the result to all connected
    callbacks.

    Watcher implementations must inherit from this base class. Subclasses
    should perform any setup required in the setup method, rather than
    overriding __init__.
    """

    def __init__(self, watch_dir, compiler, args=None, kwargs=None):
        """Store initialization values and call Watcher.setup."""
        self._watch_dir = watch_dir
        self._compiler = compiler
        self._args = args or ()
        self._kwargs = kwargs or {}
        self._callbacks = set()
        self._log = _log
        self.setup()

    def setup(self):
        """Perform any setup required here.

        Rather than implement __init__, subclasses can perform any setup in
        this method.
        """
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

    def compile(self):
        """Call the Watcher's compiler."""
        self._log.debug(
            'Compiling sass...%s(*%s, **%s)',
            self._compiler,
            self._args,
            self._kwargs,
        )
        return self._compiler(*self._args, **self._kwargs)

    def compile_and_dispatch(self):
        """Compile and dispatch the resulting css to connected callbacks."""
        self._log.debug('Compiling and dispatching....')

        try:
            css = self.compile()
        except Exception:
            self._log.exception('Failed to compile...')
            return

        self.dispatch(css)

    def dispatch(self, css):
        """Dispatch css to connected callbacks"""
        self._log.debug('Dispatching callbacks...')
        for callback in self._callbacks:
            callback(css)

    def on_change(self):
        """Called when a change is detected.

        Subclasses must call this method when they detect a change. Subclasses
        may also override this method in order to manually compile and dispatch
        callbacks. For example, a Qt implementation may use signals and slots
        to ensure that compiling and executing callbacks happens in the main
        GUI thread.
        """
        self._log.debug('Change detected...')
        self.compile_and_dispatch()

    def connect(self, fn):
        """Connect a callback to this Watcher.

        All callbacks are called when a change is detected. Callbacks are
        passed the compiled css.
        """
        self._log.debug('Connecting callback: %s', fn)
        self._callbacks.add(fn)

    def disconnect(self, fn):
        """Disconnect a callback from this Watcher."""
        self._log.debug('Disconnecting callback: %s', fn)
        self._callbacks.discard(fn)