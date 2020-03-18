#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Yann Lanthony
# Copyright (c) 2017-2018 Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Setup script for qtsass."""

# Standard library imports
from io import open
import ast
import os

# Third party imports
from setuptools import find_packages, setup


# Constants
HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='qtsass'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()

    lines = data.split('\n')
    for line in lines:
        if line.startswith('__version__'):
            version = ast.literal_eval(line.split('=')[-1].strip())
            break

    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r', encoding='utf-8') as f:
        data = f.read()

    return data


setup(
    name='qtsass',
    version=get_version(),
    description='Compile SCSS files to valid Qt stylesheets.',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    author='Yann Lanthony',
    maintainer='The Spyder Project Contributors',
    maintainer_email='qtsass@spyder-ide.org',
    url='https://github.com/spyder-ide/qtsass',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points={
        'console_scripts': [
            'qtsass = qtsass.cli:main'
        ]
    },
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    install_requires=[
        'libsass',
    ],
    keywords='qt sass qtsass scss css qss stylesheets',
)
