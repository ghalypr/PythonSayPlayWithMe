import ctypes
from ctypes import Structure, c_ulong, byref


class POINT(Structure):
	_fields_ = [("x", c_ulong), ("y", c_ulong)]


p=POINT()

ctypes.windll.user32.GetCursorPos(byref(p))

print(p.x,p.y)

