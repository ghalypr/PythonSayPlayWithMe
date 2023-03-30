from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import HWND, LPCWSTR, UINT


"""
This example demonstrates how to wrap the Windows MessageBoxW function so that it supports default parameters and named arguments. The C declaration from the windows header file is this:

WINUSERAPI int WINAPI
MessageBoxW(
    HWND hWnd,
    LPCWSTR lpText,
    LPCWSTR lpCaption,
    UINT uType);

"""

prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
paramflags = (1, "hwnd", 0), (1,"text",""), (1, "caption", ""), (1, "flags", 0)
MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)


MessageBox(text="PythonSayHi",caption="Hi",flags=2)