# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Source files event handler."""

# Standard library imports
import os
import time

# Third party imports
from watchdog.events import FileSystemEventHandler


# py2 has no FileNotFoundError
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class SourceModificationEventHandler(FileSystemEventHandler):

    def __init__(self, input_file, dest_file, watched_dir, compiler):
        super(SourceModificationEventHandler, self).__init__()
        self._input_file = input_file
        self._dest_file = dest_file
        self._compiler = compiler
        self._watched_dir = watched_dir
        self._watched_extension = os.path.splitext(self._input_file)[1]

    def _recompile(self):
        i = 0
        success = False
        while i < 10 and not success:
            try:
                time.sleep(0.2)
                self._compiler(self._input_file, self._dest_file)
                success = True
            except FileNotFoundError:
                i += 1

    def on_modified(self, event):
        # On Mac, event will always be a directory.
        # On Windows, only recompile if event's file
        # has the same extension as the input file
        we_should_recompile = (
            event.is_directory and
            os.path.samefile(event.src_path, self._watched_dir) or
            os.path.splitext(event.src_path)[1] == self._watched_extension
        )
        if we_should_recompile:
            self._recompile()

    def on_created(self, event):
        if os.path.splitext(event.src_path)[1] == self._watched_extension:
            self._recompile()
