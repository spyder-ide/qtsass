# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Test qtsass cli."""

from __future__ import absolute_import

# Standard library imports
from collections import namedtuple
from os.path import basename, exists
from subprocess import PIPE, Popen
import time

# Local imports
from . import PROJECT_DIR, await_condition, example, touch


SLEEP_INTERVAL = 1
Result = namedtuple('Result', "code stdout stderr")


def indent(text, prefix='    '):
    """Like textwrap.indent"""

    return ''.join([prefix + line for line in text.splitlines(True)])


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


def kill(proc, timeout=1):
    """Kill a subprocess and return a Result obj"""

    proc.kill()
    out, err = proc.communicate()
    out = out.decode('ascii', errors="ignore")
    err = err.decode('ascii', errors="ignore")
    return Result(proc.returncode, out, err)


def format_result(result):
    """Format a subprocess Result obj"""

    out = [
        'Subprocess Report...',
        'Exit code: %s' % result.code,
    ]
    if result.stdout:
        out.append('stdout:')
        out.append(indent(result.stdout, '    '))
    if result.stderr:
        out.append('stderr:')
        out.append(indent(result.stderr, '    '))
    return '\n'.join(out)


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
        result = kill(proc)
        report = format_result(result)
        err = "Failed to compile dummy.scss\n"
        err += report
        assert False, report

    # Ensure subprocess is still alive
    assert proc.poll() is None

    # Touch input file, triggering a recompile
    created = output.mtime()
    file_modified = lambda: output.mtime() > created
    time.sleep(SLEEP_INTERVAL)
    touch(input)

    if not await_condition(file_modified):
        result = kill(proc)
        report = format_result(result)
        err = 'Modifying %s did not trigger recompile.\n' % basename(input)
        err += report
        assert False, err

    kill(proc)


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
        result = kill(proc)
        report = format_result(result)
        err = 'All expected files have not been created...'
        err += report
        assert False, err

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
        time.sleep(SLEEP_INTERVAL)
        touch(input_file)

        if not await_condition(files_modified, timeout):
            result = kill(proc)
            report = format_result(result)
            err = 'Modifying %s did not trigger recompile.\n' % filename
            err += report
            for i, f in enumerate(expected_files):
                err += str(f) + '\n'
                err += str(old_mtimes[i]) + '\n'
                err += str(f.mtime()) + '\n'
                err += str(bool(f.mtime() > old_mtimes[i])) + '\n'
            assert False, err

        return True

    assert touch_and_wait(input_full)
    assert touch_and_wait(input_partial)
    assert touch_and_wait(input_nested)

    kill(proc)


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
