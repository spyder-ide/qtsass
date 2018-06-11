# qtsass
Compile SCSS files to valid Qt stylesheets.

## Project details

[![GitHub license](https://img.shields.io/github/license/spyder-ide/qtsass.svg)](https://github.com/spyder-ide/qtsass/blob/master/LICENSE.txt)
[![Join the chat at https://gitter.im/spyder-ide/public](https://badges.gitter.im/spyder-ide/spyder.svg)](https://gitter.im/spyder-ide/public)
[![OpenCollective Backers](https://opencollective.com/spyder/backers/badge.svg?color=blue)](#backers)
[![OpenCollective Sponsors](https://opencollective.com/spyder/sponsors/badge.svg?color=blue)](#sponsors)

## Build details

[![Travis branch](https://img.shields.io/travis/spyder-ide/qtsass/master.svg)](https://travis-ci.org/spyder-ide/qtsass)
[![AppVeyor branch](https://img.shields.io/appveyor/ci/spyder-ide/qtsass/master.svg)](https://ci.appveyor.com/project/spyder-ide/qtsass)
[![Codecov branch](https://img.shields.io/codecov/c/github/spyder-ide/qtsass/master.svg)](https://codecov.io/gh/spyder-ide/qtsass)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/spyder-ide/qtsass/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/spyder-ide/qtsass/?branch=master)


## Overview

[SASS](http://sass-lang.com/) brings countless amazing features to CSS.
Besides being used in web development, CSS is also the way to stylize Qt-based desktop applications.
However, Qt's CSS has a few variations that prevent the direct use of SASS compiler.

The purpose of this tool is to fill the gap between SASS and Qt-CSS by handling those variations.

## Qt's CSS specificities

The goal of QtSASS is to be able to generate a Qt-CSS stylesheet based on a 100% valid SASS file.
This is how it deals with Qt's specifities and how you should modify your CSS stylesheet to use QtSASS.

#### "!" in selectors
Qt allows to define the style of a widget according to its states, like this:
```
QLineEdit:enabled {
...
}
```
However, a "not" state is problematic because it introduces an exclamation mark in the selector's name, which is not valid SASS/CSS:
```
QLineEdit:!editable {
...
}
```
QtSASS allows "!" in selectors' names; the SASS file is preprocessed and any occurence of `:!` is replaced by `:_qnot_` (for "Qt not"). 
However, using this feature prevents from having a 100% valid SASS file, so this support of `!` might change in the future.
This can be replaced by the direct use of the `_qnot_` keyword in your SASS file:
```
QLineEdit:_qnot_editable { # will generate QLineEdit:!editable {
...
}
```

#### qlineargradient
The qlineargradient function also has a non-valid CSS syntax.
```
qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.1 blue, stop: 0.8 green)
```
To support qlineargradient QtSASS provides a preprocessor and a SASS implementation of the qlineargradient function. The above QSS syntax will be replaced with the following:
```
qlineargradient(0, 0, 0, 1, (0.1 blue, 0.8 green))
```
You may also use this syntax directly in your QtSASS.
```
qlineargradient(0, 0, 0, 1, (0.1 blue, 0.8 green))
# the stops parameter is a list, so you can also use variables:
$stops = 0.1 blue, 0.8 green
qlineargradient(0, 0, 0, 0, $stops)
```

#### qrgba
Qt's rgba:
```
rgba(255, 128, 128, 50%)
```
is replaced by CSS rgba:
```
rgba(255, 128, 128, 0.5)
```

## Executable usage

To compile once your SASS stylesheet to a Qt compliant CSS file:
```
# If -o is omitted, output will be print to console
qtsass style.scss -o style.css
```
To use the watch mode and get your stylesheet auto recompiled on each file save:
```
# If -o is omitted, output will be print to console
qtsass style.scss -w -o style.css
```

## Contributing

Everyone is welcome to contribute!


## Backers

Support us with a monthly donation and help us continue our activities.

[![Backers](https://opencollective.com/spyder/backers.svg)](https://opencollective.com/spyder#support)


## Sponsors

Become a sponsor to get your logo on our README on Github.

[![Sponsors](https://opencollective.com/spyder/sponsors.svg)](https://opencollective.com/spyder#support)
