import time
import sys

s = f'{time.strftime("%x %X")}'
print(s)

value = "55.66"

s = f'это значение будет в кавычках: {value!r}'
print(s)

for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")
