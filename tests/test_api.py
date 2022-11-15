# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Test qtsass api."""

from __future__ import absolute_import

# Standard library imports
from os.path import exists
import logging

# Third party imports
import pytest
import sass

# Local imports
import qtsass

# Local imports
from . import EXAMPLES_DIR, PROJECT_DIR, example


COLORS_STR = """
QWidget {
    background: rgba(127, 127, 127, 100%);
    color: rgb(255, 255, 255);
}
"""
QLINEARGRADIENTS_STR = """
QWidget {
    background: qlineargradient(
        x1: 0,
        y1: 0,
        x2: 0,
        y2: 1,
        stop: 0.1 blue,
        stop: 0.8 green
    );
}
"""
QRADIANTGRADIENTS_STR = """
QWidget {
    background: qradialgradient(
        spread: repeat,
        cx: 0,
        cy: 0,
        fx: 0,
        fy: 1,
        stop: 0.1 blue,
        stop: 0.8 green
    );
}
"""
QNOT_STR = """
QLineEdit:!editable {
    background: white;
}
"""
IMPORT_STR = """
@import 'dummy';
"""
CUSTOM_BORDER_STR = """
QWidget {
    border: custom_border();
}
"""


def setup_module():
    qtsass.enable_logging(level=logging.DEBUG)


def teardown_module():
    qtsass.enable_logging(level=logging.WARNING)


def test_compile_strings():
    """compile various strings."""

    qtsass.compile(COLORS_STR)
    qtsass.compile(QLINEARGRADIENTS_STR)
    qtsass.compile(QRADIANTGRADIENTS_STR)
    qtsass.compile(QNOT_STR)


def test_compile_import_raises():
    """compile string with import raises."""

    with pytest.raises(sass.CompileError):
        qtsass.compile(IMPORT_STR)


def test_compile_import_with_include_paths():
    """compile string with include_paths"""

    qtsass.compile(IMPORT_STR, include_paths=[EXAMPLES_DIR])


def test_compile_raises_ValueError():
    """compile raises ValueError with invalid arguments"""

    # Pass invalid type to importers - must be sequence
    with pytest.raises(ValueError):
        qtsass.compile(COLORS_STR, importers=lambda x: None)

    # Pass invalid type to custom_functions
    with pytest.raises(ValueError):
        qtsass.compile(COLORS_STR, custom_functions=lambda x: None)


def test_compile_custom_function():
    """compile string with custom_functions"""

    custom_str = (
        'QWidget {\n'
        '    border: custom_border();\n'
        '}'
    )

    def custom_border():
        return '1px solid'

    css = qtsass.compile(custom_str, custom_functions=[custom_border])
    assert '1px solid' in css
    assert 'custom_border()' not in css


def test_compile_filename(tmpdir):
    """compile_filename simple."""

    output = tmpdir.join('dummy.css')
    qtsass.compile_filename(example('dummy.scss'), output.strpath)
    assert exists(output.strpath)


def test_compile_filename_no_save():
    """compile_filename simple."""

    qss = qtsass.compile_filename(example('dummy.scss'))
    assert isinstance(qss, str)


def test_compile_filename_imports(tmpdir):
    """compile_filename with imports."""

    output = tmpdir.join('dark.css')
    qtsass.compile_filename(example('complex', 'dark.scss'), output.strpath)
    assert exists(output.strpath)


def test_compile_filename_imports_no_save():
    """compile_filename with imports."""

    qss = qtsass.compile_filename(example('complex', 'dark.scss'))
    assert isinstance(qss, str)


def test_compile_dirname(tmpdir):
    """compile_dirname complex."""

    output = tmpdir.join('complex')
    qtsass.compile_dirname(example('complex'), output.strpath)
    assert exists(output.join('dark.css').strpath)
    assert exists(output.join('light.css').strpath)


def test_watch_raises_ValueError(tmpdir):
    """watch raises ValueError when source does not exist."""

    # Watch file does not raise
    _ = qtsass.watch(example('dummy.scss'), tmpdir.join('dummy.scss').strpath)

    # Watch dir does not raise
    _ = qtsass.watch(example('complex'), tmpdir.join('complex').strpath)

    with pytest.raises(ValueError):
        _ = qtsass.watch('does_not_exist', 'does_not_exist')
