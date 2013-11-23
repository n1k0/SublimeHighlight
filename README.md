SublimeHighlight
================

*Sublime Text 3 users:* a `python3` branch is also available. Just `git checkout python3`
from the root of your package installation to use in in ST3. If you upgrade from a previous
ST2 installation or encounter problems with the package, please proceed as detailed below:

- Remove the package, if installed, using Package Control.
- Add a repository: `https://github.com/n1k0/SublimeHighlight/tree/python3`
- Install `SublimeHighlight` with Package Control. It should pull the correct branch from Github.
- Restart Sublime Text 3

This [SublimeText2](http://www.sublimetext.com/2) package allows to highlight &
export currently edited code to HTML or RTF using [Pygments](http://pygments.org/).

Several commands are added to SublimeText2 when installed:

- **SublimeHighlight: convert to HTML**: will convert current code to
  highlighted HTML in a new SublimeText tab.
- **SublimeHighlight: convert to RTF**: will convert current code to
  highlighted RTF in a new SublimeText tab.
- **SublimeHighlight: view as HTML**: will convert current code to highlighted
  HTML and open it in your default browser.
- **SublimeHighlight: view as RTF**: will convert current code to an RTF
  document and open the generated file with your default program.
- **SublimeHighlight: copy to clipboard as HTML**: will convert current code to
  highlighted HTML and store it into the system clipboard.
- **SublimeHighlight: copy to clipboard as RTF**: will convert current code to
  raw highlighted RTF and store it into the system clipboard.

This latter command, *Copy to clipboard as RTF*, allows to copy and paste highlighted
code from Sublime Tex 2 to other softwares like Powerpoint, Keynotes, Word, etc.

![capture](http://f.cl.ly/items/0p0w3w3y2V3P2v1H0q1a/SublimeHighlight.png)

Settings
--------

You can find a dedicated user settings file in the `Preferences > Package
Settings > SublimeHighlight` menu where you can customize Pygments settings:

Sample `Settings - User` file:

    {
        "theme": "monokai",
        "linenos": "inline",
        "noclasses": true,
        "fontface": "Menlo"
    }

Check out the available options below.

### Themes

You can choose the Pygments theme to use by setting the `theme` option:

    {
        "theme": "vim"
    }

Available themes are:

- `autumn`
- `borland`
- `bw`
- `colorful`
- `default`
- `emacs`
- `friendly`
- `fruity`
- `manni`
- `monokai`
- `murphy`
- `native`
- `pastie`
- `perldoc`
- `rrt`
- `tango`
- `trac`
- `vim`
- `vs`

Here's a screenshot of what some example code looks like with different themes:

![Themes Screenshot](https://raw.github.com/n1k0/SublimeHighlight/master/themes.png)

**Note:** You can add your own pygments files by copying the `_theme_.py` to `Packages/Highlight/pygments/styles`, and adding your theme to the `STYLES_MAP` in `SublimeHighlight/pygments/styles/__init__.py`.  Eg.:

    # Maps style names to 'submodule::classname'.
    STYLE_MAP = {
        'default':  'default::DefaultStyle',
        'mytheme':  'mytheme::MyThemeStyle',
    }

### Line numbering

You can add line numbering by setting the `linenos` option:

    {
        "linenos": "inline"
    }

Accepted values for the `linenos` option are `table`, `inline` or `false` — the latter being the default.

### Inline styling

You can set the rendered HTML code to use inline styles instead of CSS classes:

    {
        "noclasses": true
    }

### Lexer options

SublimeHighlight supports [Pygments lexer options](http://pygments.org/docs/lexers/). To set an option for a given lexer, eg. `PHP`:

    {
        "lexer_options": {
            "PHP": {
                "startinline": true
            }
        }
    }

### Font face

You can set font face used in RTF output by using the fontface setting.

    {
        "fontface": "Menlo"
    }

Setting up shortcuts
--------------------

This is a sample key binding for copying RTF highlighted code contents to your clipboard by pressing <kbd>ctrl</kbd> + <kbd>alt</kbd> + <kbd>c</kbd>:

```json
[
    { "keys": ["ctrl+alt+c"],
      "command": "sublime_highlight",
      "args": { "target": "clipboard",
                "output_type": "rtf"
    }},
]
```

You can combine the `target` and `output_type` argument values to achieve the stuff you want. Possible values are:

`target`:

- `sublime`: new Sublime Text 2 tab
- `external`: new external file
- `clipboard`: system clipboard

`output_type`:

- `rtf`: RTF format
- `html`: HTML format


Why this package?
-----------------

Mostly for toying around with [SublimeText2 plugin API](http://www.sublimetext.com/docs/2/api_reference.html)
(which is great), but also to ease the process of copying/pasting richly
formatted code over softwares like Powerpoint, Word, Keynote and shits like
that.

License
-------

This software is released under the terms of the [MIT license](http://en.wikipedia.org/wiki/MIT_License).
