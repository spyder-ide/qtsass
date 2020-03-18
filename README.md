# QtSASS: Compile SCSS files to Qt stylesheets

[![License - MIT](https://img.shields.io/github/license/spyder-ide/qtsass.svg)](./LICENSE.txt)
[![OpenCollective Backers](https://opencollective.com/spyder/backers/badge.svg?color=blue)](#backers)
[![Join the chat at https://gitter.im/spyder-ide/public](https://badges.gitter.im/spyder-ide/spyder.svg)](https://gitter.im/spyder-ide/public)<br>
[![Github build status](https://github.com/spyder-ide/qtsass/workflows/Tests/badge.svg)](https://github.com/spyder-ide/qtsass/actions)
[![Codecov coverage](https://img.shields.io/codecov/c/github/spyder-ide/qtsass/master.svg)](https://codecov.io/gh/spyder-ide/qtsass)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/spyder-ide/qtsass/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/spyder-ide/qtsass/?branch=master)

*Copyright © 2015 Yann Lanthony*

*Copyright © 2017–2018 Spyder Project Contributors*


## Overview

[SASS](http://sass-lang.com/) brings countless amazing features to CSS.
Besides being used in web development, CSS is also the way to stylize Qt-based desktop applications.
However, Qt's CSS has a few variations that prevent the direct use of SASS compiler.

The purpose of this tool is to fill the gap between SASS and Qt-CSS by handling those variations.


## Qt's CSS specificities

The goal of QtSASS is to be able to generate a Qt-CSS stylesheet based on a 100% valid SASS file.
This is how it deals with Qt's specifics and how you should modify your CSS stylesheet to use QtSASS.

#### "!" in selectors
Qt allows to define the style of a widget according to its states, like this:

```css
QLineEdit:enabled {
...
}
```

However, a "not" state is problematic because it introduces an exclamation mark in the selector's name, which is not valid SASS/CSS:

```css
QLineEdit:!editable {
...
}
```

QtSASS allows "!" in selectors' names; the SASS file is preprocessed and any occurence of `:!` is replaced by `:_qnot_` (for "Qt not").
However, using this feature prevents from having a 100% valid SASS file, so this support of `!` might change in the future.
This can be replaced by the direct use of the `_qnot_` keyword in your SASS file:

```css
QLineEdit:_qnot_editable { /* will generate QLineEdit:!editable { */
...
}
```

#### qlineargradient
The qlineargradient function also has a non-valid CSS syntax.

```css
qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.1 blue, stop: 0.8 green)
```

To support qlineargradient QtSASS provides a preprocessor and a SASS implementation of the qlineargradient function. The above QSS syntax will be replaced with the following:

```css
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

```css
rgba(255, 128, 128, 50%)
```

is replaced by CSS rgba:

```css
rgba(255, 128, 128, 0.5)
```


## Executable usage

To compile your SASS stylesheet to a Qt compliant CSS file:

```bash
# If -o is omitted, output will be printed to console
qtsass style.scss -o style.css
```

To use the watch mode and get your stylesheet auto recompiled on each file save:

```bash
# If -o is omitted, output will be print to console
qtsass style.scss -o style.css -w
```

To compile a directory containing SASS stylesheets to Qt compliant CSS files:

```bash
qtsass ./static/scss -o ./static/css
```

You can also use watch mode to watch the entire directory for changes.

```bash
qtsass ./static/scss -o ./static/css -w
```

Set the Environment Variable QTSASS_DEBUG to 1 or pass the --debug flag to enable logging.

```bash
qtsass ./static/scss -o ./static/css --debug
```

## API methods

### `compile(string, **kwargs)`

Conform and Compile QtSASS source code to CSS.

This function conforms QtSASS to valid SCSS before passing it to
sass.compile. Any keyword arguments you provide will be combined with
qtsass's default keyword arguments and passed to sass.compile.

Examples:

```bash
>>> import qtsass
>>> qtsass.compile("QWidget {background: rgb(0, 0, 0);}")
QWidget {background:black;}
```

Arguments:
- string: QtSASS source code to conform and compile.
- kwargs: Keyword arguments to pass to sass.compile

Returns:
- Qt compliant CSS string

### `compile_filename(input_file, dest_file, **kwargs)`:

Compile and save QtSASS file as Qt compliant CSS.

Examples:

```bash
>>> import qtsass
>>> qtsass.compile_filename('dummy.scss', 'dummy.css')
```

Arguments:
- input_file: Path to QtSass file.
- dest_file: Path to destination Qt compliant CSS file.
- kwargs: Keyword arguments to pass to sass.compile

### `compile_filename(input_file, output_file, **kwargs)`:

Compile and save QtSASS file as Qt compliant CSS.

Examples:

```bash
>>> import qtsass
>>> qtsass.compile_filename('dummy.scss', 'dummy.css')
```

Arguments:
- input_file: Path to QtSass file.
- output_file: Path to write Qt compliant CSS.
- kwargs: Keyword arguments to pass to sass.compile

### `compile_dirname(input_dir, output_dir, **kwargs)`:

Compiles QtSASS files in a directory including subdirectories.

```bash
>>> import qtsass
>>> qtsass.compile_dirname("./scss", "./css")
```

Arguments:
- input_dir: Path to directory containing QtSass files.
- output_dir: Directory to write compiled Qt compliant CSS files to.
- kwargs: Keyword arguments to pass to sass.compile

### `enable_logging(level=None, handler=None)`:
Enable logging for qtsass.

Sets the qtsass logger's level to:
    1. the provided logging level
    2. logging.DEBUG if the QTSASS_DEBUG envvar is a True value
    3. logging.WARNING

```bash
>>> import logging
>>> import qtsass
>>> handler = logging.StreamHandler()
>>> formatter = logging.Formatter('%(level)-8s: %(name)s> %(message)s')
>>> handler.setFormatter(formatter)
>>> qtsass.enable_logging(level=logging.DEBUG, handler=handler)
```

Arguments:
- level: Optional logging level
- handler: Optional handler to add

### `watch(source, destination, compiler=None, Watcher=None)`:
Watches a source file or directory, compiling QtSass files when modified.

The compiler function defaults to compile_filename when source is a file
and compile_dirname when source is a directory.

Arguments:
- source: Path to source QtSass file or directory.
- destination: Path to output css file or directory.
- compiler: Compile function (optional)
- Watcher: Defaults to qtsass.watchers.Watcher (optional)

Returns:
- qtsass.watchers.Watcher instance

## Contributing

Everyone is welcome to contribute!


## Sponsors

Spyder and its subprojects are funded thanks to the generous support of

[![Quansight](https://static.wixstatic.com/media/095d2c_2508c560e87d436ea00357abc404cf1d~mv2.png/v1/crop/x_0,y_9,w_915,h_329/fill/w_380,h_128,al_c,usm_0.66_1.00_0.01/095d2c_2508c560e87d436ea00357abc404cf1d~mv2.png)](https://www.quansight.com/)[![Numfocus](https://i2.wp.com/numfocus.org/wp-content/uploads/2017/07/NumFocus_LRG.png?fit=320%2C148&ssl=1)](https://numfocus.org/)


and the donations we have received from our users around the world through [Open Collective](https://opencollective.com/spyder/):

[![Sponsors](https://opencollective.com/spyder/sponsors.svg)](https://opencollective.com/spyder#support)

Please consider becoming a sponsor!
