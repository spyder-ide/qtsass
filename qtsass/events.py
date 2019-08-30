# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Source files event handler."""

try:
    # yapf: disable

    # Third party imports
    from watchdog.events import FileSystemEventHandler

    # yapf: enable
    class SourceEventHandler(FileSystemEventHandler):
        """File handler to call sass compiler on_modified event."""

        def __init__(self, source, destination, compiler):
            """
            :param str source: String path to qss source file.
            :param str source: String path to compiled target file.
            :param function compiler: Function object to call when
                source was modified.
            """
            super(SourceEventHandler, self).__init__()
            self._source = source
            self._destination = destination
            self._compiler = compiler

        def on_modified(self, _event):
            """Calls sass compiler function object"""
            self._compiler(self._source, self._destination)

except ImportError:
    SourceEventHandler = None
