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

    @property
    def code(self):
        return self.view.substr(self.region)

    @property
    def encoding(self):
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'utf-8'
        elif encoding == 'Western (Windows 1252)':
            encoding = 'windows-1252'
        return encoding

    @property
    def region(self):
        regions = self.view.sel()
        if len(regions) > 0 and regions[0].size() > 0:
            return regions[0]
        else:
            return sublime.Region(0, self.view.size())

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

    def get_formatter(self, output_type, style="vim", full=True):
        return get_formatter_by_name(output_type, style=style, full=full)

    def get_lexer(self, code=None):
        code = code if code is not None else self.code
        lexer = None
        if self.view.file_name():
            try:
                lexer = get_lexer_for_filename(self.view.file_name(), code)
            except ClassNotFound:
                pass
        if not lexer:
            lexer = self.guess_lexer_from_syntax()
        if not lexer:
            lexer = guess_lexer(code)
        return lexer

    def highlight(self, output_type):
        return pygments.highlight(self.code, self.get_lexer(),
            self.get_formatter(output_type))

    def run(self, edit, target='external', output_type='html'):
        output_type = output_type if output_type in FORMATS else 'html'
        pygmented = self.highlight(output_type)

        if target == 'external':
            filename = '%s.%s' % (self.view.id(), output_type,)
            tmp_file = self.write_file(filename, pygmented)
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

    def write_file(self, filename, contents, encoding=None):
        """Writes highlighted contents onto the filesystem."""
        encoding = encoding if encoding is not None else self.encoding
        tmp_fullpath = os.path.join(tempfile.gettempdir(), filename)
        tmp_file = open(tmp_fullpath, 'w')
        tmp_file.write(contents.encode(encoding))
        tmp_file.close()
        return tmp_fullpath
