#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based off of http://stackoverflow.com/a/3429034/334717
# and http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/file/4c7503da2658/win32/src/win32clipboardmodule.cpp

import ctypes
from ctypes import c_int, c_size_t, c_wchar, c_void_p, sizeof, memmove

# Get required functions.
ocb = ctypes.windll.user32.OpenClipboard  # Basic Clipboard functions
ecb = ctypes.windll.user32.EmptyClipboard
gcd = ctypes.windll.user32.GetClipboardData
scd = ctypes.windll.user32.SetClipboardData
rcf = ctypes.windll.user32.RegisterClipboardFormatA
ccb = ctypes.windll.user32.CloseClipboard
ga = ctypes.windll.kernel32.GlobalAlloc    # Global Memory allocation
ga.restype = c_void_p
gl = ctypes.windll.kernel32.GlobalLock     # Global Memory Locking
gl.restype = c_void_p
gul = ctypes.windll.kernel32.GlobalUnlock
gle = ctypes.windll.kernel32.GetLastError
GHND = 0x0042

CF_HTML = rcf("HTML Format".encode())
CF_RTF = rcf("Rich Text Format".encode())
CF_RTFWO = rcf("Rich Text Format Without Objects".encode())
CF_TEXT = 1
CF_UNICODETEXT = 13

def Paste(data, type='text', plaintext=None):
    if plaintext is None:
        plaintext = data

    if type == 'html':
        data = EncodeHTML(data)

    data = data.encode('utf-8', 'replace')

    unicodetext = plaintext.encode('utf_16')
    plaintext = plaintext.encode('cp1252', 'replace')

    ocb(c_void_p(0))  # Open Clip, Default task
    ecb()

    if type == 'rtf':
        Put(data, CF_RTF)
    elif type == 'html':
        Put(data, CF_HTML)

    ccb()


def Put(data, format):
    # Ensure we are using a bytes object.
    data = bytes(data)
    # Allocate global memory, including space for terminator.
    # GHND is GMEM_MOVEABLE (required) and GMEM_ZEROINIT (convenient).
    hCd = ga(c_int(GHND), c_size_t(len(data) + sizeof(c_wchar())))

    # Lock the memory and get a pointer to it.
    pchData = gl(c_void_p(hCd))
    if not pchData:
        code = gle()
        raise Exception('Failed to lock: %r' % code)

    # Move data into global memory.
    memmove(c_void_p(pchData), data, c_size_t(len(data)))
    # Unlock.
    gul(c_void_p(hCd))
    # Set clipboard data.
    scd(c_int(format), c_void_p(hCd))


# Based off of http://code.activestate.com/recipes/474121-getting-html-from-the-windows-clipboard/
def EncodeHTML(fragment):
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
