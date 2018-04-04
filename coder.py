from algebra import bigint, euclidean
from primes import long_primes, fermi
from time import time


def generate():
    p, q = long_primes()
    n = p * q
    fi = (p - bigint.one()) * (q - bigint.one())
    e = bigint.one()
    d = bigint.one()
    for i in range(2, 5):
        try:
            e = fermi(i)
            d = e.inverse(fi)
            break
        except:
            print "gcd({}, {}) is not 1!".format(fi, e)
    log = "\
        exp\t e = {}\n\
        inverse\t d = {}\n\
        mult\t n = {}\n\
        euler\tfi = {}\n".format(e, d, n, fi)
    return {
        "log": log,
        "public": (e, n),
        "private": (d, n)
    }


def code(m, key):
    return m.mod_pow(key[0], key[1])


def decode(c, key):
    start = time()
    return c.mod_pow(key[0], key[1]), time() - start


m = bigint.from_dec(228)

keys = generate()

print keys["log"]
print "message: {}".format(m)
c = code(m, keys["public"])
print "coded: {}".format(c)
res = decode(c, keys['private'])
print "decoded: {}\ntime: {}".format(res[0], res[1])
