# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Test qtsass cli."""

# Standard library imports
from __future__ import absolute_import
import os
import time
import signal
import sys
from os.path import exists, basename
from textwrap import dedent
from subprocess import Popen, PIPE
from collections import namedtuple

#Local imports
from . import PROJECT_DIR, example, touch, await_condition


Result = namedtuple('Result', "code stdout stderr")


def invoke(args):
    """Invoke qtsass cli with specified args"""

    kwargs = dict(
        stdout=PIPE,
        stderr=PIPE,
        cwd=PROJECT_DIR
    )
    proc = Popen(['python', '-m', 'qtsass'] + args, **kwargs)
    return proc


def invoke_with_result(args):
    """Invoke qtsass cli and return a Result obj"""

    proc = invoke(args)
    out, err = proc.communicate()
    out = out.decode('ascii', errors="ignore")
    err = err.decode('ascii', errors="ignore")
    return Result(proc.returncode, out, err)


def test_compile_dummy_to_stdout():
    """CLI compile dummy example to stdout."""

    args = [example('dummy.scss')]
    result = invoke_with_result(args)

    assert result.code == 0
    assert result.stdout


def test_compile_dummy_to_file(tmpdir):
    """CLI compile dummy example to file."""

    input = example('dummy.scss')
    output = tmpdir.join('dummy.css')
    args = [input, '-o', output.strpath]
    result = invoke_with_result(args)

    assert result.code == 0
    assert exists(output.strpath)


def test_watch_dummy(tmpdir):
    """CLI watch dummy example."""

    input = example('dummy.scss')
    output = tmpdir.join('dummy.css')
    args = [input, '-o', output.strpath, '-w']
    proc = invoke(args)

    # Wait for initial compile
    output_exists = lambda: exists(output.strpath)
    if not await_condition(output_exists):
        proc.terminate()
        assert False, "Failed to compile dummy.scss"

    # Ensure subprocess is still alive
    assert proc.poll() is None

    # Touch input file, triggering a recompile
    created = output.mtime()
    file_modified = lambda: output.mtime() > created
    time.sleep(0.1)
    touch(input)

    if not await_condition(file_modified):
        proc.terminate()
        assert False, 'Output file has not been recompiled...'

    proc.terminate()


def test_compile_complex(tmpdir):
    """CLI compile complex example."""

    input = example('complex')
    output = tmpdir.mkdir('output')
    args = [input, '-o', output.strpath]
    result = invoke_with_result(args)

    assert result.code == 0

    expected_files = [output.join('light.css'), output.join('dark.css')]
    for file in expected_files:
        assert exists(file.strpath)


def test_watch_complex(tmpdir):
    """CLI watch complex example."""

    input = example('complex')
    output = tmpdir.mkdir('output')
    args = [input, '-o', output.strpath, '-w']
    proc = invoke(args)

    expected_files = [output.join('light.css'), output.join('dark.css')]

    # Wait for initial compile
    files_created = lambda: all([exists(f.strpath) for f in expected_files])
    if not await_condition(files_created):
        assert False, 'All expected files have not been created...'

    # Ensure subprocess is still alive
    assert proc.poll() is None

    # Input files to touch
    input_full = example('complex', 'light.scss')
    input_partial = example('complex', '_base.scss')
    input_nested = example('complex', 'widgets', '_qwidget.scss')

    def touch_and_wait(input_file, timeout=2000):
        """Touch a file, triggering a recompile"""

        filename = basename(input_file)
        old_mtimes = [f.mtime() for f in expected_files]
        files_modified = lambda: all(
            [f.mtime() > old_mtimes[i] for i, f in enumerate(expected_files)]
        )
        time.sleep(0.1)
        touch(input_file)

        if not await_condition(files_modified, timeout):
            proc.terminate()
            err = 'Modifying %s did not trigger recompile.' % filename
            assert False, err

        return True

    assert touch_and_wait(input_full)
    assert touch_and_wait(input_partial)
    assert touch_and_wait(input_nested)

    proc.terminate()


def test_invalid_input():
    """CLI input is not a file or dir."""

    proc = invoke_with_result(['file_does_not_exist.scss'])
    assert proc.code == 1
    assert 'Error: input must be' in proc.stdout

    proc = invoke_with_result(['./dir/does/not/exist'])
    assert proc.code == 1
    assert 'Error: input must be' in proc.stdout


def test_dir_missing_output():
    """CLI dir missing output option"""

    proc = invoke_with_result([example('complex')])
    assert proc.code == 1
    assert 'Error: missing required option' in proc.stdout
