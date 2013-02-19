#Based off of http://stackoverflow.com/a/3429034/334717

import ctypes

#Get required functions, strcpy..
strcpy = ctypes.cdll.msvcrt.strcpy
ocb = ctypes.windll.user32.OpenClipboard    #Basic Clipboard functions
ecb = ctypes.windll.user32.EmptyClipboard
gcd = ctypes.windll.user32.GetClipboardData
scd = ctypes.windll.user32.SetClipboardData
rcf = ctypes.windll.user32.RegisterClipboardFormatA
ccb = ctypes.windll.user32.CloseClipboard
ga = ctypes.windll.kernel32.GlobalAlloc    # Global Memory allocation
gl = ctypes.windll.kernel32.GlobalLock     # Global Memory Locking
gul = ctypes.windll.kernel32.GlobalUnlock
GMEM_DDESHARE = 0x2000

CF_HTML = rcf("HTML Format")
CF_RTF = rcf("Rich Text Format")
CF_RTFWO = rcf("Rich Text Format Without Objects")
CF_TEXT = 1


def Get():
    ocb(None)  # Open Clip, Default task
    pcontents = gcd(1)  # 1 means CF_TEXT.. too lazy to get the token thingy ...
    data = ctypes.c_char_p(pcontents).value
    #gul(pcontents) ?
    ccb()

    return data


def Paste(data, type, plaintext):
    plaintext = plaintext.encode('cp1252')
    ocb(None)  # Open Clip, Default task
    ecb()

    hCd = ga(GMEM_DDESHARE, len(bytes(data)) + 1)
    hPd = ga(GMEM_DDESHARE, len(bytes(plaintext)) + 1)

    pchData = gl(hCd)
    ptxData = gl(hPd)

    strcpy(ctypes.c_char_p(pchData), bytes(data))
    strcpy(ctypes.c_char_p(ptxData), bytes(plaintext))

    gul(hCd)
    gul(hPd)

    if type == 'rtf':
        scd(1, hPd)
        scd(CF_RTF, hCd, 0, False)
        scd(CF_RTFWO, hCd, 0, False)
    elif type == 'text':
        scd(1, hCd)
    elif type == 'html':
        scd(1, hPd)
        scd(CF_HTML, hCd, 0, False)

    ccb()
