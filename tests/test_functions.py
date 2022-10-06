# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Test qtsass custom functions."""

from __future__ import absolute_import

# Standard library imports
import unittest

# Local imports
from qtsass.api import compile


class BaseCompileTest(unittest.TestCase):
    def compile_scss(self, string):
        # NOTE: revise for better future compatibility
        wstr = '*{{t: {0};}}'.format(string)
        res = compile(wstr)
        return res.replace('* {\n  t: ', '').replace('; }\n', '')


class TestRgbaFunc(BaseCompileTest):
    def test_rgba(self):
        self.assertEqual(
            self.compile_scss('rgba(0, 1, 2, 0.3)'),
            'rgba(0, 1, 2, 30%)'
        )

    def test_rgba_percentage_alpha(self):
        result = self.compile_scss('rgba(255, 0, 125, 75%)')
        self.assertEqual(result, 'rgba(255, 0, 125, 75%)')

    def test_rgba_8bit_int_alpha(self):
        for in_val, out_val in ((0, 0), (128, 50), (255, 100)):
            result = self.compile_scss('rgba(255, 0, 125, %i)' % in_val)
            self.assertEqual(result, 'rgba(255, 0, 125, %i%%)' % out_val)


class TestQLinearGradientFunc(BaseCompileTest):
    def test_color(self):
        self.assertEqual(
            self.compile_scss('qlineargradient(1, 2, 3, 4, (0 red, 1 blue))'),
            'qlineargradient(x1: 1.0, y1: 2.0, x2: 3.0, y2: 4.0, '
            'stop: 0.0 rgba(255, 0, 0, 100%), stop: 1.0 rgba(0, 0, 255, 100%))'
        )

    def test_rgba(self):
        self.assertEqual(
            self.compile_scss('qlineargradient(1, 2, 3, 4, (0 red, 0.2 rgba(5, 6, 7, 0.8)))'),
            'qlineargradient(x1: 1.0, y1: 2.0, x2: 3.0, y2: 4.0, '
            'stop: 0.0 rgba(255, 0, 0, 100%), stop: 0.2 rgba(5, 6, 7, 80%))'
        )


class TestQRadialGradientFunc(BaseCompileTest):
    def test_color(self):
        self.assertEqual(
            self.compile_scss('qradialgradient(pad, 1, 2, 1, 3, 4, (0 red, 1 blue))'),
            'qradialgradient(spread: pad, cx: 1.0, cy: 2.0, radius: 1.0, fx: 3.0, fy: 4.0, '
            'stop: 0.0 rgba(255, 0, 0, 100%), stop: 1.0 rgba(0, 0, 255, 100%))'
        )

    def test_rgba(self):
        self.assertEqual(
            self.compile_scss('qradialgradient(pad, 1, 2, 1, 3, 4, (0 red, 0.2 rgba(5, 6, 7, 0.8)))'),
            'qradialgradient(spread: pad, cx: 1.0, cy: 2.0, radius: 1.0, fx: 3.0, fy: 4.0, '
            'stop: 0.0 rgba(255, 0, 0, 100%), stop: 0.2 rgba(5, 6, 7, 80%))'
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
