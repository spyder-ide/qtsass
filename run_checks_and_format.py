#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Run checks and format code."""

# yapf: disable

# Standard library imports
from subprocess import PIPE, Popen
import os
import sys


# yapf: enable

# Constants
PY3 = sys.version[0] == '3'
COMMANDS = [
    ['pydocstyle', 'qtsass'],
    ['pycodestyle', 'qtsass'],
    ['yapf', 'qtsass', '--in-place', '--recursive'],
    ['isort', '-y'],
]


def run_process(cmd_list):
    """Run popen process."""

    try:
        p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
    except OSError:
        raise OSError('Could not call command list: "%s"' % cmd_list)

    out, err = p.communicate()
    if PY3:
        out = out.decode()
        err = err.decode()
    return out, err


def repo_changes():
    """Check if repo files changed."""
    out, _err = run_process(['git', 'status', '--short'])
    out_lines = [l for l in out.split('\n') if l.strip()]
    return out_lines


def run():
    """Run linters and formatters."""

    for cmd_list in COMMANDS:
        cmd_str = ' '.join(cmd_list)
        print('\nRunning: ' + cmd_str)

        out, err = run_process(cmd_list)
        if out:
            print(out)
        if err:
            print(err)

    out_lines = repo_changes()
    if out_lines:
        print('\nPlease run the linter and formatter script!')
        print('\n'.join(out_lines))
        code = 1
    else:
        print('\nAll checks passed!')
        code = 0

    print('\n')
    sys.exit(code)


if __name__ == '__main__':
    run()
