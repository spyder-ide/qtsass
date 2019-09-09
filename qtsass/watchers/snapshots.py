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
import os

# Local imports
from qtsass.importers import norm_path


# yapf: enable


def take(dir_or_file, depth=3):
    """Return a dict mapping files and folders to their mtimes."""
    if os.path.isfile(dir_or_file):
        path = norm_path(dir_or_file)
        return {path: os.path.getmtime(path)}

    if not os.path.isdir(dir_or_file):
        return {}

    snapshot = {}
    base_depth = len(norm_path(dir_or_file).split('/'))

    for root, subdirs, files in os.walk(dir_or_file):

        path = norm_path(root)
        if len(path.split('/')) - base_depth == depth:
            subdirs[:] = []

        snapshot[path] = os.path.getmtime(path)
        for f in files:
            path = norm_path(root, f)
            snapshot[path] = os.path.getmtime(path)

    return snapshot


def diff(prev_snapshot, next_snapshot):
    """Return a dict containing changes between two snapshots."""
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
