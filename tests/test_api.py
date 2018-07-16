# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Test qtsass api."""

# Standard library imports
from __future__ import absolute_import
from os.path import exists

# Third party imports
import pytest
import sass

# Local imports
from . import PROJECT_DIR, EXAMPLES_DIR, example
import qtsass


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


def test_compile_strings():
    """compile various strings."""

    qtsass.compile(COLORS_STR)
    qtsass.compile(QLINEARGRADIENTS_STR)
    qtsass.compile(QNOT_STR)


def test_compile_import_raises():
    """compile string with import raises."""

    with pytest.raises(sass.CompileError):
        qtsass.compile(IMPORT_STR)


def test_compile_import_with_include_paths():
    """compile string with include_paths"""

    qtsass.compile(IMPORT_STR, include_paths=[EXAMPLES_DIR])


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


def test_compile_filename_imports(tmpdir):
    """compile_filename with imports."""

    output = tmpdir.join('dark.css')
    qtsass.compile_filename(example('complex', 'dark.scss'), output.strpath)
    assert exists(output.strpath)


def test_compile_dirname(tmpdir):
    """compile_dirname complex."""

    output = tmpdir.join('complex')
    qtsass.compile_dirname(example('complex'), output.strpath)
    assert exists(output.join('dark.css').strpath)
    assert exists(output.join('light.css').strpath)
