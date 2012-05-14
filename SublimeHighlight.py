# -*- coding: utf-8 -*-

"""
    TODO:
    - add a setting to store prefered theme name
    - customize rendered HTML to ease choosing a new theme
"""

import desktop
import os
import pygments
import re
import sublime
import sublime_plugin
import sys
import tempfile

# crazy ST2 bug, see http://www.sublimetext.com/forum/viewtopic.php?f=6&t=1278
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)),
    'pygments'))

from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename,
    guess_lexer)
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound


FORMATS = ('html', 'rtf',)
HTML_TEMPLATE = u"""<!DOCTYPE html>
<html>
<meta charset="%(encoding)s">
<title>%(title)s</title>
<style>%(styles)s</style>
%(highlighted)s
"""


def get_template(**kwargs):
    return kwargs.get('template', HTML_TEMPLATE) % dict(**kwargs)


class SublimeHighlightCommand(sublime_plugin.TextCommand):
    """Code highlighter command."""

    def guess_lexer_from_syntax(self):
        syntax = self.view.settings().get('syntax')
        if not syntax:
            return
        match = re.match(r"Packages/.*/(.*?)\.tmLanguage$", syntax)
        if not match:
            return
        try:
            return get_lexer_by_name(match.group(1).lower())
        except ClassNotFound:
            return

    def run(self, edit, target='external', output_type='html'):
        if len(self.view.sel()) > 0:
            region = self.view.sel()[0]
        else:
            region = sublime.Region(0, self.view.size())
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'utf-8'
        elif encoding == 'Western (Windows 1252)':
            encoding = 'windows-1252'
        code = self.view.substr(region)

        # pygmentize the code
        output_type = output_type if output_type in FORMATS else 'html'
        formatter = get_formatter_by_name(output_type, style='vim', full=True)
        lexer = None
        if self.view.file_name():
            lexer = get_lexer_for_filename(self.view.file_name(), code)
        if not lexer:
            lexer = self.guess_lexer_from_syntax()
        if not lexer:
            lexer = guess_lexer(code)
        pygmented = pygments.highlight(code, lexer, formatter)

        if target == 'external':
            filename = '%s.%s' % (self.view.id(), output_type,)
            tmp_file = self.write_file(filename, pygmented, encoding=encoding)
            sublime.status_message(tmp_file)
            desktop.open(tmp_file)
        elif target == 'clipboard':
            sublime.set_clipboard(pygmented)
        elif target == 'sublime':
            new_view = self.view.window().new_file()
            if output_type == 'html':
                new_view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
            new_edit = new_view.begin_edit()
            new_view.insert(new_edit, 0, pygmented)
            new_view.end_edit(new_edit)

    def write_file(self, filename, contents, encoding='utf-8'):
        """Writes highlighted contents onto the filesystem."""
        tmp_fullpath = os.path.join(tempfile.gettempdir(), filename)
        tmp_file = open(tmp_fullpath, 'w')
        tmp_file.write(contents.encode(encoding))
        tmp_file.close()
        return tmp_fullpath
