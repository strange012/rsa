import time
import random


def fib(n):
    if n == 1:
        return 1

    def rec(m):
        if m == 2:
            return (1, 1)
        else:
            x, y = rec(m - 1)
            return (y, x + y)
    return rec(n)[1]


def gen_int(n):
    s = "1"
    for _ in range(n - 1):
        time.sleep(0.001119)
        a = "%.18f" % time.time()
        a = int(a[len(a) - 18:])
        s += str((a % 239) % 2)
    return s


for i in range(0, 10):
    print(gen_int(100))
