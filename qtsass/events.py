# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Source files event handler."""

# yapf: disable

# Third party imports
from watchdog.events import FileSystemEventHandler


# yapf: enable

class SourceEventHandler(FileSystemEventHandler):
    """Source event hanlder."""

    def __init__(self, source, destination, compiler):
        """Source event hanlder."""
        super(SourceEventHandler, self).__init__()
        self._source = source
        self._destination = destination
        self._compiler = compiler

    def on_modified(self, event):
        """Override watchdog method to handle on file modification events."""
        self._compiler(self._source, self._destination)
