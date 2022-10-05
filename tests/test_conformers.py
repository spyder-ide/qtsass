# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Test qtsass conformers."""

from __future__ import absolute_import

# Standard library imports
from textwrap import dedent
import unittest

# Local imports
from qtsass.conformers import (
    NotConformer,
    QLinearGradientConformer,
    QRadialGradientConformer,
)


class TestNotConformer(unittest.TestCase):

    qss_str = 'QAbstractItemView::item:!active'
    css_str = 'QAbstractItemView::item:_qnot_active'

    def test_conform_to_scss(self):
        """NotConformer qss to scss."""

        c = NotConformer()
        self.assertEqual(c.to_scss(self.qss_str), self.css_str)

    def test_conform_to_qss(self):
        """NotConformer css to qss."""

        c = NotConformer()
        self.assertEqual(c.to_qss(self.css_str), self.qss_str)

    def test_round_trip(self):
        """NotConformer roundtrip."""

        c = NotConformer()
        conformed_css = c.to_scss(self.qss_str)
        self.assertEqual(c.to_qss(conformed_css), self.qss_str)


class TestQLinearGradientConformer(unittest.TestCase):

    css_vars_str = 'qlineargradient($x1, $y1, $x2, $y2, (0 $red, 1 $blue))'
    qss_vars_str = (
        'qlineargradient(x1:$x1, x2:$x2, y1:$y1, y2:$y2'
        'stop: 0 $red, stop: 1 $blue)'
    )

    css_nostops_str = 'qlineargradient(0, 0, 0, 0)'
    qss_nostops_str = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0)'

    css_str = 'qlineargradient(0, 0, 0, 0, (0 red, 1 blue))'
    qss_singleline_str = (
        'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0, '
        'stop: 0 red, stop: 1 blue)'
    )
    qss_multiline_str = dedent("""
    qlineargradient(
        x1: 0,
        y1: 0,
        x2: 0,
        y2: 0,
        stop: 0 red,
        stop: 1 blue
    )
    """).strip()
    qss_weird_whitespace_str = (
        'qlineargradient( x1: 0, y1:0, x2: 0, y2:0, '
        '   stop:0 red, stop: 1 blue )'
    )

    css_rgba_str = (
        'qlineargradient(0, 0, 0, 0, '
        '(0 rgba(0, 1, 2, 30%), 0.99 rgba(7, 8, 9, 100%)))'
    )
    qss_rgba_str = (
        'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0, '
        'stop: 0 rgba(0, 1, 2, 30%), stop: 0.99 rgba(7, 8, 9, 100%))'
    )

    css_incomplete_coords_str = (
        'qlineargradient(0, 1, 0, 0, (0 red, 1 blue))'
    )

    qss_incomplete_coords_str = (
        'qlineargradient(y1:1, stop:0 red, stop: 1 blue)'
    )

    css_float_coords_str = (
        'qlineargradient(0, 0.75, 0, 0, (0 green, 1 pink))'
    )

    qss_float_coords_str = (
        'qlineargradient(y1:0.75, stop:0 green, stop: 1 pink)'
    )

    def test_does_not_affect_css_form(self):
        """QLinearGradientConformer no affect on css qlineargradient func."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.css_str), self.css_str)
        self.assertEqual(c.to_qss(self.css_str), self.css_str)

    def test_conform_singleline_str(self):
        """QLinearGradientConformer singleline qss to scss."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_singleline_str), self.css_str)

    def test_conform_multiline_str(self):
        """QLinearGradientConformer multiline qss to scss."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_multiline_str), self.css_str)

    def test_conform_weird_whitespace_str(self):
        """QLinearGradientConformer weird whitespace qss to scss."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_weird_whitespace_str), self.css_str)

    def test_conform_nostops_str(self):
        """QLinearGradientConformer qss with no stops to scss."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_nostops_str), self.css_nostops_str)

    def test_conform_vars_str(self):
        """QLinearGradientConformer qss with vars to scss."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_vars_str), self.css_vars_str)

    def test_conform_rgba_str(self):
        """QLinearGradientConformer qss with rgba to scss."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_rgba_str), self.css_rgba_str)

    def test_incomplete_coords(self):
        """QLinearGradientConformer qss with not all 4 coordinates given."""

        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_incomplete_coords_str),
                         self.css_incomplete_coords_str)

    def test_float_coords(self):
        c = QLinearGradientConformer()
        self.assertEqual(c.to_scss(self.qss_float_coords_str),
                         self.css_float_coords_str)


class TestQRadialGradientConformer(unittest.TestCase):

    css_vars_str = "qradialgradient('$spread', $cx, $cy, $radius, $fx, $fy, (0 $red, 1 $blue))"
    qss_vars_str = (
        'qradialgradient(spread:$spread, cx:$cx, cy:$cy, radius:$radius, fx:$fx, fy:$fy,'
        'stop: 0 $red, stop: 1 $blue)'
    )

    css_nostops_str = "qradialgradient('pad', 0, 0, 0, 0, 0)"
    qss_nostops_str = 'qradialgradient(spread: pad, cx: 0, cy: 0, fx: 0, fy: 0)'

    css_str = "qradialgradient('pad', 0, 0, 0, 0, 0, (0 red, 1 blue))"
    qss_singleline_str = (
        'qradialgradient(spread: pad, cx: 0, cy: 0, fx: 0, fy: 0, '
        'stop: 0 red, stop: 1 blue)'
    )
    qss_multiline_str = dedent("""
    qradialgradient(
        spread: pad,
        cx: 0,
        cy: 0,
        fx: 0,
        fy: 0,
        stop: 0 red,
        stop: 1 blue
    )
    """).strip()
    qss_weird_whitespace_str = (
        'qradialgradient( spread: pad, cx: 0, cy:0, fx: 0, fy:0, '
        '   stop:0 red, stop: 1 blue )'
    )

    css_rgba_str = (
        "qradialgradient('pad', 0, 0, 0, 0, 0, "
        "(0 rgba(0, 1, 2, 30%), 0.99 rgba(7, 8, 9, 100%)))"
    )
    qss_rgba_str = (
        'qradialgradient(spread: pad, cx: 0, cy: 0, fx: 0, fy: 0, '
        'stop: 0 rgba(0, 1, 2, 30%), stop: 0.99 rgba(7, 8, 9, 100%))'
    )

    css_incomplete_coords_str = (
        "qradialgradient('pad', 0, 1, 0, 0, 0, (0 red, 1 blue))"
    )

    qss_incomplete_coords_str = (
        'qradialgradient(spread:pad, cy:1, stop:0 red, stop: 1 blue)'
    )

    css_float_coords_str = (
        "qradialgradient('pad', 0, 0.75, 0, 0, 0, (0 green, 1 pink))"
    )

    qss_float_coords_str = (
        'qradialgradient(spread: pad, cy:0.75, stop:0 green, stop: 1 pink)'
    )

    def test_does_not_affect_css_form(self):
        """QRadialGradientConformer no affect on css qradialgradient func."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.css_str), self.css_str)
        self.assertEqual(c.to_qss(self.css_str), self.css_str)

    def test_conform_singleline_str(self):
        """QRadialGradientConformer singleline qss to scss."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_singleline_str), self.css_str)

    def test_conform_multiline_str(self):
        """QRadialGradientConformer multiline qss to scss."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_multiline_str), self.css_str)

    def test_conform_weird_whitespace_str(self):
        """QRadialGradientConformer weird whitespace qss to scss."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_weird_whitespace_str), self.css_str)

    def test_conform_nostops_str(self):
        """QRadialGradientConformer qss with no stops to scss."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_nostops_str), self.css_nostops_str)

    def test_conform_vars_str(self):
        """QRadialGradientConformer qss with vars to scss."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_vars_str), self.css_vars_str)

    def test_conform_rgba_str(self):
        """QRadialGradientConformer qss with rgba to scss."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_rgba_str), self.css_rgba_str)

    def test_incomplete_coords(self):
        """QRadialGradientConformer qss with not all 4 coordinates given."""

        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_incomplete_coords_str),
                         self.css_incomplete_coords_str)

    def test_float_coords(self):
        c = QRadialGradientConformer()
        self.assertEqual(c.to_scss(self.qss_float_coords_str),
                         self.css_float_coords_str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
