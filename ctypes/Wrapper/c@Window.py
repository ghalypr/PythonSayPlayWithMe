"""

look at https://stackoverflow.com/questions/5353883/python3-ctype-createwindowex-simple-example


"""


#coding:utf8
from __future__ import unicode_literals

import sys
from ctypes import *
from ctypes import wintypes as w  # ctypes has many pre-defined Windows types

def errcheck(result,func,args):
    if result is None or result == 0:
        raise WinError(get_last_error())
    return result

# Missing from ctypes.wintypes...
LRESULT = c_int64
HCURSOR = c_void_p

WNDPROC = WINFUNCTYPE(LRESULT,w.HWND,w.UINT,w.WPARAM,w.LPARAM)

def MAKEINTRESOURCEW(x):
    return w.LPCWSTR(x)

class WNDCLASSW(Structure):
    _fields_ = [('style', w.UINT),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', w.HINSTANCE),
                ('hIcon', w.HICON),
                ('hCursor', HCURSOR),
                ('hbrBackground', w.HBRUSH),
                ('lpszMenuName', w.LPCWSTR),
                ('lpszClassName', w.LPCWSTR)]

class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', w.HDC),
                ('fErase', w.BOOL),
                ('rcPaint', w.RECT),
                ('fRestore', w.BOOL),
                ('fIncUpdate', w.BOOL),
                ('rgbReserved', w.BYTE * 32)]

kernel32 = WinDLL('kernel32',use_last_error=True)
kernel32.GetModuleHandleW.argtypes = w.LPCWSTR,
kernel32.GetModuleHandleW.restype = w.HMODULE
kernel32.GetModuleHandleW.errcheck = errcheck

user32 = WinDLL('user32',use_last_error=True)
user32.CreateWindowExW.argtypes = w.DWORD,w.LPCWSTR,w.LPCWSTR,w.DWORD,c_int,c_int,c_int,c_int,w.HWND,w.HMENU,w.HINSTANCE,w.LPVOID
user32.CreateWindowExW.restype = w.HWND
user32.CreateWindowExW.errcheck = errcheck
user32.LoadIconW.argtypes = w.HINSTANCE,w.LPCWSTR
user32.LoadIconW.restype = w.HICON
user32.LoadIconW.errcheck = errcheck
user32.LoadCursorW.argtypes = w.HINSTANCE,w.LPCWSTR
user32.LoadCursorW.restype = HCURSOR
user32.LoadCursorW.errcheck = errcheck
user32.RegisterClassW.argtypes = POINTER(WNDCLASSW),
user32.RegisterClassW.restype = w.ATOM
user32.RegisterClassW.errcheck = errcheck
user32.ShowWindow.argtypes = w.HWND,c_int
user32.ShowWindow.restype = w.BOOL
user32.UpdateWindow.argtypes = w.HWND,
user32.UpdateWindow.restype = w.BOOL
user32.UpdateWindow.errcheck = errcheck
user32.GetMessageW.argtypes = POINTER(w.MSG),w.HWND,w.UINT,w.UINT
user32.GetMessageW.restype = w.BOOL
user32.TranslateMessage.argtypes = POINTER(w.MSG),
user32.TranslateMessage.restype = w.BOOL
user32.DispatchMessageW.argtypes = POINTER(w.MSG),
user32.DispatchMessageW.restype = LRESULT
user32.BeginPaint.argtypes = w.HWND,POINTER(PAINTSTRUCT)
user32.BeginPaint.restype = w.HDC
user32.BeginPaint.errcheck = errcheck
user32.GetClientRect.argtypes = w.HWND,POINTER(w.RECT)
user32.GetClientRect.restype = w.BOOL
user32.GetClientRect.errcheck = errcheck
user32.DrawTextW.argtypes = w.HDC,w.LPCWSTR,c_int,POINTER(w.RECT),w.UINT
user32.DrawTextW.restype = c_int
user32.EndPaint.argtypes = w.HWND,POINTER(PAINTSTRUCT)
user32.EndPaint.restype = w.BOOL
user32.PostQuitMessage.argtypes = c_int,
user32.PostQuitMessage.restype = None
user32.DefWindowProcW.argtypes = w.HWND,w.UINT,w.WPARAM,w.LPARAM
user32.DefWindowProcW.restype = LRESULT

gdi32 = WinDLL('gdi32',use_last_error=True)
gdi32.GetStockObject.argtypes = c_int,
gdi32.GetStockObject.restype = w.HGDIOBJ

CW_USEDEFAULT = -2147483648
IDI_APPLICATION = MAKEINTRESOURCEW(32512)
WS_OVERLAPPEDWINDOW = 13565952

CS_HREDRAW = 2
CS_VREDRAW = 1

IDC_ARROW = MAKEINTRESOURCEW(32512)
WHITE_BRUSH = 0

SW_SHOWNORMAL = 1

WM_PAINT = 15
WM_DESTROY = 2
DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4

def MainWin():
    # Define Window Class
    wndclass = WNDCLASSW()
    wndclass.style          = CS_HREDRAW | CS_VREDRAW
    wndclass.lpfnWndProc    = WNDPROC(WndProc)
    wndclass.cbClsExtra = wndclass.cbWndExtra = 0
    wndclass.hInstance      = kernel32.GetModuleHandleW(None)
    wndclass.hIcon          = user32.LoadIconW(None, IDI_APPLICATION)
    wndclass.hCursor        = user32.LoadCursorW(None, IDC_ARROW)
    wndclass.hbrBackground  = gdi32.GetStockObject(WHITE_BRUSH)
    wndclass.lpszMenuName   = None
    wndclass.lpszClassName  = 'MainWin'

    # Register Window Class
    user32.RegisterClassW(byref(wndclass))

    # Create Window
    hwnd = user32.CreateWindowExW(0,
                          wndclass.lpszClassName,
                          'Python Window',
                          WS_OVERLAPPEDWINDOW,
                          CW_USEDEFAULT,
                          CW_USEDEFAULT,
                          CW_USEDEFAULT,
                          CW_USEDEFAULT,
                          None,
                          None,
                          wndclass.hInstance,
                          None)
    # Show Window
    user32.ShowWindow(hwnd,SW_SHOWNORMAL)
    user32.UpdateWindow(hwnd)

    # Pump Messages
    msg = w.MSG()
    while user32.GetMessageW(byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(byref(msg))
        user32.DispatchMessageW(byref(msg))

    return msg.wParam

def WndProc(hwnd, message, wParam, lParam):
    ps = PAINTSTRUCT()
    rect = w.RECT()

    if message == WM_PAINT:
        hdc = user32.BeginPaint(hwnd,byref(ps))
        user32.GetClientRect(hwnd,byref(rect))
        user32.DrawTextW(hdc,
                         'Python Powered Windows 你好吗？',
                         -1, byref(rect), 
                         DT_SINGLELINE|DT_CENTER|DT_VCENTER)
        user32.EndPaint(hwnd,byref(ps))
        return 0
    elif message == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0

    return user32.DefWindowProcW(hwnd,message,wParam,lParam)

if __name__=='__main__':
    sys.exit(MainWin())