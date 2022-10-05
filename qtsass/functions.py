# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Libsass functions."""

# yapf: disable

# Third party imports
import sass


# yapf: enable


def rgba(r, g, b, a):
    """Convert r,g,b,a values to standard format.

    Where `a` is alpha! In CSS alpha can be given as:
     * float from 0.0 (fully transparent) to 1.0 (opaque)
    In Qt or qss that is:
     * int from 0 (fully transparent) to 255 (opaque)
    A percentage value 0% (fully transparent) to 100% (opaque) works
    in BOTH systems the same way!
    """
    result = 'rgba({}, {}, {}, {}%)'
    if isinstance(r, sass.SassNumber):
        if a.unit == '%':
            alpha = a.value
        elif a.value > 1.0:
            # A value from 0 to 255 is coming in, convert to %
            alpha = a.value / 2.55
        else:
            alpha = a.value * 100
        return result.format(
            int(r.value),
            int(g.value),
            int(b.value),
            int(alpha),
        )
    elif isinstance(r, float):
        return result.format(int(r), int(g), int(b), int(a * 100))


def rgba_from_color(color):
    """
    Conform rgba.

    :type color: sass.SassColor
    """
    # Inner rgba() call
    if not isinstance(color, sass.SassColor):
        return '{}'.format(color)

    return rgba(color.r, color.g, color.b, color.a)


def qlineargradient(x1, y1, x2, y2, stops):
    """
    Implement qss qlineargradient function for scss.

    :type x1: sass.SassNumber
    :type y1: sass.SassNumber
    :type x2: sass.SassNumber
    :type y2: sass.SassNumber
    :type stops: sass.SassList
    :return:
    """
    stops_str = []
    for stop in stops[0]:
        pos, color = stop[0]
        stops_str.append('stop: {} {}'.format(
            pos.value,
            rgba_from_color(color),
        ))
    template = 'qlineargradient(x1: {}, y1: {}, x2: {}, y2: {}, {})'
    return template.format(x1.value, y1.value, x2.value, y2.value,
                           ', '.join(stops_str))


def qradialgradient(spread, cx, cy, radius, fx, fy, stops):
    """
    Implement qss qradialgradient function for scss.

    :type spread: string
    :type cx: sass.SassNumber
    :type cy: sass.SassNumber
    :type radius: sass.SassNumber
    :type fx: sass.SassNumber
    :type fy: sass.SassNumber
    :type stops: sass.SassList
    :return:
    """
    stops_str = []
    for stop in stops[0]:
        pos, color = stop[0]
        stops_str.append('stop: {} {}'.format(
            pos.value,
            rgba_from_color(color),
        ))
    template = ('qradialgradient('
                'spread: {}, cx: {}, cy: {}, radius: {}, fx: {}, fy: {}, {}'
                ')')
    return template.format(spread, cx.value, cy.value, radius.value, fx.value,
                           fy.value, ', '.join(stops_str))
