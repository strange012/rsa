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
