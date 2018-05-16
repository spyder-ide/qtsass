# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Conform qss to compliant scss and css to valid qss."""

# Standard library imports
from __future__ import absolute_import, print_function
import re


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
        """Replaces "!" in selectors with "_qnot_"."""

        return qss.replace(':!', ':_qnot_')

    def to_qss(self, css):
        """Replaces "_qnot_" in selectors with "!"."""

        return css.replace(':_qnot_', ':!')


class QLinearGradientConformer(Conformer):
    """Conform QSS qlineargradient function."""

    qss_pattern = re.compile(
        'qlineargradient\('
        '((?:(?:\s+)?(?:x1|y1|x2|y2):(?:\s+)?[0-9A-Za-z$_-]+,?)+)'  # coords
        '((?:(?:\s+)?stop:.*,?)+(?:\s+)?)?'  # stops
        '\)',
        re.MULTILINE
    )

    def _conform_group_to_scss(self, group):
        """
        Takes a qss str containing xy coords or stops and returns a str
        containing just the values.

        'x1: 0, y1: 0, x2: 0, y2: 0' => '0, 0, 0, 0'
        'stop: 0 red, stop: 1 blue' => '0 red, 1 blue'
        """
        new_group = []
        for part in group.strip().split(','):
            if part:
                _, value = part.split(':')
                new_group.append(value.strip())
        return ', '.join(new_group)

    def to_scss(self, qss):
        """
        Conform qss qlineargradient to scss qlineargradient form.

        Normalizes all whitespace including the removal of newline chars.

        qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0, stop: 0 red, stop: 1 blue)
        =>
        qlineargradient(0, 0, 0, 0, (0 red, 1 blue))
        """

        conformed = qss

        for coords, stops in self.qss_pattern.findall(qss):

            new_coords = self._conform_group_to_scss(coords)
            conformed = conformed.replace(coords, new_coords, 1)

            if not stops:
                continue

            new_stops = ', ({})'.format(self._conform_group_to_scss(stops))
            conformed = conformed.replace(stops, new_stops, 1)

        return conformed

    def to_qss(self, css):
        """Handled by qlineargradient function passed to sass.compile"""

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
