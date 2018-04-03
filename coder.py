from algebra import bigint, euclidean
from primes import long_primes, fermi

p, q = long_primes()
n = p * q
fi = (p - bigint.one()) * (q - bigint.one())
e = fermi(2)
d = e.inverse(fi)
print (d)
# print "e*d mod fi = {}".format(e * d % fi)
