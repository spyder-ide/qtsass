# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Conform qss to compliant scss and css to valid qss."""

# yapf: disable

from __future__ import absolute_import, print_function

# Standard library imports
import re


# yapf: enable


class Conformer(object):
    """Base class for all text transformations."""

    def to_scss(self, qss):
        """Transform some qss to valid scss."""
        return NotImplemented

    def to_qss(self, css):
        """Transform some css to valid qss."""
        return NotImplemented


class NotConformer(Conformer):
    """Conform QSS "!" in selectors."""

    def to_scss(self, qss):
        """Replace "!" in selectors with "_qnot_"."""
        return qss.replace(':!', ':_qnot_')

    def to_qss(self, css):
        """Replace "_qnot_" in selectors with "!"."""
        return css.replace(':_qnot_', ':!')


class QLinearGradientConformer(Conformer):
    """Conform QSS qlineargradient function."""

    _DEFAULT_COORDS = ('x1', 'y1', 'x2', 'y2')

    qss_pattern = re.compile(
        r'qlineargradient\('
        r'((?:(?:\s+)?(?:x1|y1|x2|y2):(?:\s+)?[0-9A-Za-z$_\.-]+,?)+)'  # coords
        r'((?:(?:\s+)?stop:.*,?)+(?:\s+)?)?'  # stops
        r'\)',
        re.MULTILINE,
    )

    def _conform_coords_to_scss(self, group):
        """
        Take a qss str with xy coords and returns the values.

          'x1: 0, y1: 0, x2: 0, y2: 0' => '0, 0, 0, 0'
          'y1: 1' => '0, 1, 0, 0'
        """
        values = ['0', '0', '0', '0']
        for key_values in [part.split(':', 1) for part in group.split(',')]:
            try:
                key, value = key_values
                key = key.strip()
                if key in self._DEFAULT_COORDS:
                    pos = self._DEFAULT_COORDS.index(key)
                    if pos >= 0 and pos <= 3:
                        values[pos] = value.strip()
            except ValueError:
                pass
        return ', '.join(values)

    def _conform_stops_to_scss(self, group):
        """
        Take a qss str with stops and returns the values.

          'stop: 0 red, stop: 1 blue' => '0 red, 1 blue'
        """
        new_group = []
        split = [""]
        bracket_level = 0
        for char in group:
            if not bracket_level and char == ",":
                split.append("")
                continue
            elif char == "(":
                bracket_level += 1
            elif char == ")":
                bracket_level -= 1
            split[-1] += char

        for part in split:
            if part:
                _, value = part.split(':', 1)
                new_group.append(value.strip())
        return ', '.join(new_group)

    def to_scss(self, qss):
        """
        Conform qss qlineargradient to scss qlineargradient form.

        Normalize all whitespace including the removal of newline chars.

        qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0, stop: 0 red, stop: 1 blue)
        =>
        qlineargradient(0, 0, 0, 0, (0 red, 1 blue))
        """
        conformed = qss

        for coords, stops in self.qss_pattern.findall(qss):
            new_coords = self._conform_coords_to_scss(coords)
            conformed = conformed.replace(coords, new_coords, 1)

            if not stops:
                continue

            new_stops = ', ({})'.format(self._conform_stops_to_scss(stops))
            conformed = conformed.replace(stops, new_stops, 1)

        return conformed

    def to_qss(self, css):
        """Transform to qss from css."""
        return css


class QRadialGradientConformer(Conformer):
    """Conform QSS qradialgradient function."""

    _DEFAULT_COORDS = ('cx', 'cy', 'radius', 'fx', 'fy')

    qss_pattern = re.compile(
        r'qradialgradient\('
        # spread
        r'((?:(?:\s+)?(?:spread):(?:\s+)?[0-9A-Za-z$_\.-]+,?)+)?'
        # coords
        r'((?:(?:\s+)?(?:cx|cy|radius|fx|fy):(?:\s+)?[0-9A-Za-z$_\.-]+,?)+)'
        # stops
        r'((?:(?:\s+)?stop:.*,?)+(?:\s+)?)?'
        r'\)',
        re.MULTILINE,
    )

    def _conform_spread_to_scss(self, group):
        """
        Take a qss str with xy coords and returns the values.

          'spread: pad|repeat|reflect'
        """
        value = 'pad'
        for key_values in [part.split(':', 1) for part in group.split(',')]:
            try:
                key, value = key_values
                key = key.strip()
                if key == 'spread':
                    value = value.strip()
            except ValueError:
                pass
        return value

    def _conform_coords_to_scss(self, group):
        """
        Take a qss str with xy coords and returns the values.

          'cx: 0, cy: 0, radius: 0, fx: 0, fy: 0' => '0, 0, 0, 0, 0'
          'cy: 1' => '0, 1, 0, 0, 0'
        """
        values = ['0', '0', '0', '0', '0']
        for key_values in [part.split(':', 1) for part in group.split(',')]:
            try:
                key, value = key_values
                key = key.strip()
                if key in self._DEFAULT_COORDS:
                    pos = self._DEFAULT_COORDS.index(key)
                    if pos >= 0:
                        values[pos] = value.strip()
            except ValueError:
                pass
        return ', '.join(values)

    def _conform_stops_to_scss(self, group):
        """
        Take a qss str with stops and returns the values.

          'stop: 0 red, stop: 1 blue' => '0 red, 1 blue'
        """
        new_group = []
        split = [""]
        bracket_level = 0
        for char in group:
            if not bracket_level and char == ",":
                split.append("")
                continue
            elif char == "(":
                bracket_level += 1
            elif char == ")":
                bracket_level -= 1
            split[-1] += char

        for part in split:
            if part:
                _, value = part.split(':', 1)
                new_group.append(value.strip())
        return ', '.join(new_group)

    def to_scss(self, qss):
        """
        Conform qss qradialgradient to scss qradialgradient form.

        Normalize all whitespace including the removal of newline chars.

        qradialgradient(cx: 0, cy: 0, radius: 0,
                        fx: 0, fy: 0, stop: 0 red, stop: 1 blue)
        =>
        qradialgradient(0, 0, 0, 0, 0, (0 red, 1 blue))
        """
        conformed = qss

        for spread, coords, stops in self.qss_pattern.findall(qss):
            new_spread = "'" + self._conform_spread_to_scss(spread) + "', "
            conformed = conformed.replace(spread, new_spread, 1)
            new_coords = self._conform_coords_to_scss(coords)
            conformed = conformed.replace(coords, new_coords, 1)
            if not stops:
                continue

            new_stops = ', ({})'.format(self._conform_stops_to_scss(stops))
            conformed = conformed.replace(stops, new_stops, 1)

        return conformed

    def to_qss(self, css):
        """Transform to qss from css."""
        return css


conformers = [c() for c in Conformer.__subclasses__() if c is not Conformer]


def scss_conform(input_str):
    """
    Conform qss to valid scss.

    Runs the to_scss method of all Conformer subclasses on the input_str.
    Conformers are run in order of definition.

    :param input_str: QSS string
    :returns: Valid SCSS string
    """
    conformed = input_str
    for conformer in conformers:
        conformed = conformer.to_scss(conformed)

    return conformed


def qt_conform(input_str):
    """
    Conform css to valid qss.

    Runs the to_qss method of all Conformer subclasses on the input_str.
    Conformers are run in reverse order.

    :param input_str: CSS string
    :returns: Valid QSS string
    """
    conformed = input_str
    for conformer in conformers[::-1]:
        conformed = conformer.to_qss(conformed)

    return conformed
