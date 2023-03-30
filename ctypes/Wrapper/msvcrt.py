from ctypes import *


libc = windll.msvcrt
printf = libc.printf
sscanf = libc.sscanf


printf(b"Hello, %s\n", b"World!")


i = c_int()
f = c_float()
s = create_string_buffer(b'000'*32)

sscanf(b"1 3.14 Hello",b"%d %f %s",byref(i),byref(f),byref(s))

print(i.value,f.value,s.value)

