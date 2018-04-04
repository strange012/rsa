from functools import reduce
from conventer import bin_to_dec, dec_to_bin
import copy


def myprint(mylist):
    print [str(x) for x in mylist]


class bigint:
    neg = False
    num = []

    def __init__(self, num):
        self.num = list(num)
        self.num.reverse()
        self.neg *= not self.is_zero()

    def get_reversed(self):
        return bigint(self.num)

    def __neg__(self):
        a = copy.deepcopy(self)
        a.neg = not a.neg
        return a

    def __pos__(self):
        a = copy.deepcopy(self)
        a.neg = False
        return a

    @classmethod
    def one(cls):
        return cls([1])

    @classmethod
    def zero(cls):
        return cls([0])

    def is_zero(self):
        return not (len(self) - 1 + self.num[0])

    @classmethod
    def from_str(cls, s):
        a = cls([int(x) for x in s if x != "-"])
        a.neg = True if s[0] == "-" else False
        return a

    @classmethod
    def from_dec(cls, dec):
        return cls.from_str(dec_to_bin(dec))

    def __len__(self):
        return len(self.num)

    def __str__(self):
        return str(bin_to_dec(("-" if self.neg else "") + reduce((lambda x, y: str(y) + x), self.num, "")))

    def __add__(self, other):
        if self.neg ^ other.neg:
            return self - (-other)
        carry = 0
        a = copy.deepcopy(self)
        for i in range(0, max(len(a.num), len(other.num))):
            if (i == len(a.num)):
                a.num.append(0)

            a.num[i] = carry + a.num[i] + \
                (other.num[i] if i < len(other.num) else 0)
            carry = a.num[i] / 2
            a.num[i] = a.num[i] % 2
        if carry:
            a.num.append(carry)
        a.neg *= not a.is_zero()
        return a

    def __mul__(self, other):
        res = [0] * (len(self.num) + len(other.num))
        for i in range(0, len(self.num)):
            for j in range(0, len(other.num)):
                res[i + j] += self.num[i] * other.num[j]
        for i in range(0, len(self.num) + len(other.num) - 1):
            res[i + 1] += res[i] / 2
            res[i] = res[i] % 2
        while ((len(res) > 1) and (res[-1] == 0)):
            res.pop()
        a = bigint(res).get_reversed()
        a.neg = (self.neg ^ other.neg) * (not a.is_zero())
        return a

    def __sub__(self, other):
        if self.neg ^ other.neg:
            return self + (-other)
        carry = 0
        i = 0
        a = copy.deepcopy(max(+self, +other))
        b = min(+self, +other)
        a.neg = self < other
        while i in range(0, len(a.num)) or carry:
            a.num[i] -= (b.num[i] if i < len(b.num) else 0) + carry
            carry = a.num[i] < 0
            a.num[i] = a.num[i] % 2
            i += 1
        while ((len(a.num) > 1) and (a.num[-1] == 0)):
            a.num.pop()
        a.neg *= not a.is_zero()
        return a

    def __eq__(self, other):
        return self.num == other.num and self.neg == other.neg

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.neg > other.neg:
            return True
        if self.neg < other.neg:
            return False
        if self.neg * other.neg:
            return (+other) < (+self)
        if (len(self) > len(other)):
            return False
        if (len(self) < len(other)):
            return True
        for i in range(len(self) - 1, -1, -1):
            if self.num[i] != other.num[i]:
                return self.num[i] < other.num[i]
        return False

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

    def division(self, other):
        if self < other:
            return bigint([0]), self
        if self.neg + other.neg != 0:
            raise TypeError("dividing negative values")
        a = copy.deepcopy(self)
        b = copy.deepcopy(other)
        b << (len(a) - len(b))
        quot = []

        while len(b) >= len(other) and (not b.is_zero()):
            if a >= b:
                a -= b
                quot.append(1)
            else:
                quot.append(0)
            b >> 1
        q = bigint(quot)
        while ((len(q) > 1) and (q.num[-1] == 0)):
            q.num.pop()
        return q, a

    def __div__(self, other):
        return self.division(other)[0]

    def __mod__(self, other):
        return self.division(other)[1]

    def __lshift__(self, shift):
        self.num = [0] * shift + self.num
        return self

    def __rshift__(self, shift):
        if len(self) <= shift:
            self.num = bigint.zero().num
            self.neg = False
        else:
            self.num = self.num[shift:]
        return self

    def __pow__(self, other):
        if self.neg != 0:
            raise TypeError("dividing negative values")
        exp = copy.deepcopy(other)
        a = copy.deepcopy(self)
        res = bigint.one()
        while exp > bigint.zero():
            if exp.num[0] == 1:
                res *= a
                exp -= bigint.one()
            else:
                a *= a
                exp >> 1
        return res

    def mod_mul(self, other, module):
        res = bigint.zero()
        for i in range(len(self) - 1, -1, -1):
            res = res * bigint.from_dec(2)
            if res >= module:
                res -= module
            if self.num[i]:
                res = res + other
            if (res >= module):
                res -= module
        return res

    def mod_pow(self, exponent, module):
        if self.neg != 0:
            raise TypeError("Dividing negative integers.")
        exp = copy.deepcopy(exponent)
        a = copy.deepcopy(self)
        res = bigint.one()
        while exp > bigint.zero():
            if exp.num[0] == 1:
                res = (res * a) % module
                # res = res.mod_mul(a, module)
                exp -= bigint.one()
            else:
                a = (a * a) % module
                # a = a.mod_mul(a, module)
                exp >> 1
        return res

    def inverse(self, module):
        x, y, d = euclidean(self, module)
        if d != bigint.one():
            raise TypeError(
                "Inappropriate method!\nCan't find inverse element of not coprime integers.")
        return x if x >= bigint.zero() else x + module


def euclidean(a, b):
    def rec(a, b):
        q, r = a.division(b)
        if r.is_zero():
            return bigint.one(), bigint.zero(), b
        x, y, d = rec(b, r)
        return y - q * x, x, d
    x, y, d = rec(max(a, b), min(a, b))
    return (x, y, d) if a < b else (y, x, d)


###########################################################

# x = bigint.from_dec(3)
# p = bigint.from_dec(31)

# print "x: {}".format(x)
# print "p: {}".format(p)
# a = x.inverse(p)
# print "a: {}".format(x.inverse(p))
# print "{}*{} mod {} = {}".format(x, a, p, (x * a) % p)

###########################################################
# import time

# a = bigint.from_dec(57)
# p = bigint.from_dec(239)

# exp = p - bigint.one()
# print "a: {}".format(a)
# print "p: {}".format(p)
# print "p-1: {}".format(exp)

# start = time.time()
# res = a**exp
# print "a**p-1: {}\n{}s".format(res, time.time() - start)

# start = time.time()
# t = res / p
# print "a**exp / p: {}\n{}s".format(t, time.time() - start)

# start = time.time()
# t = a.mod_pow(exp, p)
# print "a**p-1 mod p (mod pow): {}\n{}s".format(t,  time.time() - start)
