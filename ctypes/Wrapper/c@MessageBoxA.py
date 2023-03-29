import ctypes

"""

 look at the documentation for MessageboxA on Microsoft's site

https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox?redirectedfrom=MSDN

"""





# buttons
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000

# icons
ICON_EXCLAIM = 0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

result = ctypes.windll.user32.MessageBoxA(0, b"Hi User . read the documentation", b"user32 func", MB_HELP | MB_YESNO | ICON_STOP)

## Ye 6
## No 7
## Help not responding
print(result)
