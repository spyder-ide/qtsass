# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Source files event handler."""

# Third party imports
from watchdog.events import FileSystemEventHandler


class SourceEventHandler(FileSystemEventHandler):

    def __init__(self, source, destination, compiler):
        super(SourceEventHandler, self).__init__()
        self._source = source
        self._destination = destination
        self._compiler = compiler

    def on_modified(self, event):
        self._compiler(self._source, self._destination)
