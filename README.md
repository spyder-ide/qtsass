# qtsass
Compile SCSS files to valid Qt stylesheets.

[SASS](http://sass-lang.com/) brings countless amazing features to CSS.
Besides being used in web development, CSS is also the way to stylize Qt-based desktop applications.
However, Qt's CSS has a few variations that prevent the direct use of SASS compiler.

The purpose of this tool is to fill the gap between SASS and Qt-CSS by handling those variations.

## Qt's CSS specificities
WIP 

"!" in selectors

qlineargradient

qrgba


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
