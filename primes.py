from time import time
from conventer import bin_to_dec
import random
from algebra import bigint

p33 = 18014398241046527
q33 = 1125899839733759

p60 = 362736035870515331128527330659
q60 = 115756986668303657898962467957

p100 = 37975227936943673922808872755445627854565536638199
q100 = 40094690950920881030683735292761468389214899724061

p129 = "100111110101000010010000001001000010101011100010001100\
110101100110010001110110011001010100110001100010000000100101100\
101110010111101110001001001100111000011000111101100000111010101\
00000011000000010010001100010010101"

q129 = "100001111100001010010110111011010100100000001111100110\
101011000101111000100001011101111011001101001100010001100101111\
101011000010111011101111001110000001101101011000111000011000011\
00100011010010011001011011100001"


def long_primes():
    return bigint.from_dec(p100), bigint.from_dec(q100)


def fermi(n):
    return bigint.from_dec(2**(2**n) + 1)


def fib(n):
    if n <= bigint.one():
        return n

    curr = bigint.one()
    prev = bigint.one()
    i = bigint.from_dec(2)
    while i < n:
        temp = curr
        curr += prev
        prev = temp
        i += bigint.one()
    return curr


def primes(n):
    pr = []
    lp = [0] * (n)
    for i in range(2, n):
        if lp[i] == 0:
            lp[i] = i
            pr += [i]
        for p in pr:
            if p > lp[i] or p * i >= n:
                break
            lp[p * i] = p
    return pr


def test_prime_fermi(n, k):
    for _ in range(0, k):
        a = gen_int(random.randint(3, len(n) - 2))
        if a.mod_pow(n - bigint.one(), n) != bigint.one():
            return False
    return True


def test_prime_fermi_fib(n):
    if n % bigint.from_dec(2) != bigint.one():
        return False
    r = n % bigint.from_dec(5)
    if not (r == bigint.from_dec(2) or r == bigint.from_dec(2)):
        return False
    if bigint.from_dec(2).mod_pow(n - bigint.one(), n) != bigint.one():
        return False
    if not (fib(n + bigint.one()) % n).is_zero():
        return False
    return True


def pair_of_primes(n, k):
    a = primes(n)[::k]
    return a[len(a) - 2:]


def gen_int(n):
    s = "1"
    for _ in range(n - 1):
        s += str(random.randint(0, 1))
    return bigint.from_str(s)


def gen_prime(n, k):
    x = bigint.zero()
    while 1:
        x = gen_int(n)
        if k == 0:
            if test_prime_fermi_fib(x):
                break
        else:
            if test_prime_fermi(x, k):
                break
    return x


for i in range(3, 4):
    start = time()
    print "{} : {}".format(i, gen_prime(100, i))
    print "time : {}".format(time() - start)
