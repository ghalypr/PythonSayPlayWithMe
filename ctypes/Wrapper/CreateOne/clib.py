import ctypes


C_Library = ctypes.WinDLL("./clib.so")

hello0x1 = C_Library.say_hello
hello0x1.argtypes=[ctypes.c_int]


num_repeats = 5

hello0x1(num_repeats)
