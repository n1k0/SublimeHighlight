#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based off of http://stackoverflow.com/a/3429034/334717
# and http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/file/4c7503da2658/win32/src/win32clipboardmodule.cpp

import ctypes
from ctypes import c_int, c_char, c_char_p, c_wchar, c_wchar_p, sizeof

# Get required functions, strcpy..
strcpy = ctypes.cdll.msvcrt.strcpy
wcscpy = ctypes.cdll.msvcrt.wcscpy
ocb = ctypes.windll.user32.OpenClipboard  # Basic Clipboard functions
ecb = ctypes.windll.user32.EmptyClipboard
gcd = ctypes.windll.user32.GetClipboardData
scd = ctypes.windll.user32.SetClipboardData
rcf = ctypes.windll.user32.RegisterClipboardFormatA
ccb = ctypes.windll.user32.CloseClipboard
ga = ctypes.windll.kernel32.GlobalAlloc    # Global Memory allocation
gl = ctypes.windll.kernel32.GlobalLock     # Global Memory Locking
gul = ctypes.windll.kernel32.GlobalUnlock
GHND = 0x0042

CF_HTML = rcf("HTML Format")
CF_RTF = rcf("Rich Text Format")
CF_RTFWO = rcf("Rich Text Format Without Objects")
CF_TEXT = 1
CF_UNICODETEXT = 13


def Get():
    ocb(None)  # Open Clip, Default task
    pcontents = gcd(1)  # 1 means CF_TEXT.. too lazy to get the token thingy ...
    data = c_char_p(pcontents).value
    #gul(pcontents) ?
    ccb()

    return data


def Paste(data, type='text', plaintext=None):
    if plaintext is None:
        plaintext = data

    if type == 'html':
        data = EncodeHTML(data)
    else:
        data = data.encode('cp1252', 'replace')

    unicodetext = plaintext.encode('utf_16')
    plaintext = plaintext.encode('cp1252', 'replace')

    ocb(None)  # Open Clip, Default task
    ecb()

    if type == 'rtf':
        Put(data, CF_RTF)
        Put(data, CF_RTFWO)
    elif type == 'html':
        Put(data, CF_HTML)

    Put(plaintext, CF_TEXT)
    Put(unicodetext, CF_UNICODETEXT)
    ccb()


def Put(data, format):
    if format == CF_UNICODETEXT:
        hCd = ga(GHND, len(bytes(data)) + sizeof(c_char()))
    else:
        hCd = ga(GHND, len(bytes(data)) + sizeof(c_wchar()))

    pchData = gl(hCd)

    if format == CF_UNICODETEXT:
        wcscpy(c_wchar_p(pchData), bytes(data))
    else:
        strcpy(c_char_p(pchData), bytes(data))
    gul(hCd)
    scd(c_int(format), hCd, 0, False)


# Based off of http://code.activestate.com/recipes/474121-getting-html-from-the-windows-clipboard/
def EncodeHTML(fragment):
    fragment = fragment.encode('utf-8', 'replace')
    DEFAULT_HTML_BODY = \
        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">" \
        "<HTML><HEAD></HEAD><BODY><!--StartFragment-->%s<!--EndFragment--></BODY></HTML>"

    MARKER_BLOCK_OUTPUT = \
        "Version:0.9\r\n" \
        "StartHTML:%09d\r\n" \
        "EndHTML:%09d\r\n" \
        "StartFragment:%09d\r\n" \
        "EndFragment:%09d\r\n"

    html = DEFAULT_HTML_BODY % fragment
    fragmentStart = html.index(fragment)
    fragmentEnd = fragmentStart + len(fragment)

    dummyPrefix = MARKER_BLOCK_OUTPUT % (0, 0, 0, 0)
    lenPrefix = len(dummyPrefix)

    prefix = MARKER_BLOCK_OUTPUT % (lenPrefix, len(html) + lenPrefix,
                    fragmentStart + lenPrefix, fragmentEnd + lenPrefix)

    return (prefix + html)
