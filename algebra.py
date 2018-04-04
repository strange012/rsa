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

    def __getitem__(self, n):
        return self.num[n]

    def __setitem__(self, n, val):
        self.num[n] = val

    def get_reversed(self):
        return bigint(self.num)

    def __neg__(self):
        a = self.copy()
        a.neg = not self.neg
        return a

    def __pos__(self):
        a = self.copy()
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
        # return str((("-" if self.neg else "") + reduce((lambda x, y: str(y) + x), self.num, "")))

    def __add__(self, other):
        if self.neg ^ other.neg:
            return self - (-other)
        carry = 0
        a = self.copy()
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

    def copy(self):
        a = bigint.zero()
        a.num = list(self.num)
        a.neg = self.neg
        return a

    def __mul__(self, other):
        ls = len(self)
        lo = len(other)
        res = [0] * (ls + lo)
        for i in range(0, ls):
            for j in range(0, lo):
                res[i + j] += self.num[i] * other.num[j]
        for i in range(0, ls + lo - 1):
            res[i + 1] += res[i] / 2
            res[i] = res[i] % 2
        while ((len(res) > 1) and (res[-1] == 0)):
            res.pop()
        a = bigint.zero()
        a.num = res
        a.neg = (self.neg ^ other.neg) * (not a.is_zero())
        return a

    def __sub__(self, other):
        if self.neg ^ other.neg:
            return self + (-other)
        carry = 0
        i = 0
        a = max(+self, +other).copy()
        b = min(+self, +other).copy()
        lb = len(b)
        a.neg = self < other
        for i in range(0, lb):
            a.num[i] -= b.num[i] + carry
            carry = a.num[i] < 0
            a.num[i] = a.num[i] % 2
        i = lb
        while carry:
            a.num[i] -= carry
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
        ls = len(self)
        lo = len(other)
        if self.neg > other.neg:
            return True
        if self.neg < other.neg:
            return False
        if self.neg * other.neg:
            return (+other) < (+self)
        if ls > lo:
            return False
        if ls < lo:
            return True
        for i in range(ls - 1, -1, -1):
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
        if self < bigint.zero() or other <= bigint.zero():
            raise TypeError("dividing negative values")
        if self < other:
            return bigint.zero(), self
        a = self.copy()
        b = other.copy()
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

    def long_division(self, other):
        if self < bigint.zero() or other <= bigint.zero():
            raise TypeError("dividing negative values")
        ln = len(self)
        if self < other:
            return bigint.zero(), self
        q = [0] * ln
        r = bigint.zero()
        for i in range(ln - 1, -1, -1):
            r << 1
            r[0] = self[i]
            if r >= other:
                r = r - other
                q[i] = 1
        quot = bigint(q).get_reversed()
        while ((len(quot) > 1) and (quot.num[-1] == 0)):
            quot.num.pop()
        return quot, r

    def rest_division(self, other):
        ls = len(self)
        r = self.copy()
        b = other.copy() << ls
        q = [0] * ls
        for i in range(ls - 1, -1, -1):
            r = bigint.from_dec(2) * r - b
            if r >= bigint.zero():
                q[i] = 1
            else:
                q[i] = 0
                r = r + b
        quot = bigint.zero()
        quot.num = q
        quot -= bigint.zero()
        return quot, r >> ls

    def non_rest_division(self, other):
        r = self.copy()
        b = other.copy() << len(self)
        q = [0] * len(self)
        for i in range(len(self) - 1, -1, -1):
            if r >= bigint.zero():
                q[i] = 1
                r = bigint.from_dec(2) * r - b
            else:
                q[i] = 0
                r = bigint.from_dec(2) * r + b
        quot = bigint.zero()
        quot.num = q
        q = [not x for x in q]
        neg = bigint.zero()
        neg.num = q
        quot = quot - neg
        if r < bigint.zero():
            quot = quot - bigint.one()
            r = r + other
        return quot, r >> len(self)

    def simple_division(self, other):
        if self <= bigint.zero() or other <= bigint.zero():
            raise TypeError("dividing negative values")
        q = bigint.zero()
        r = self.copy()
        while r >= other:
            q = q + bigint.one()
            r = r - other
        return q, r

    def __div__(self, other):
        return self.long_division(other)[0]

    def __mod__(self, other):
        return self.long_division(other)[1]

    def __lshift__(self, shift):
        if self.is_zero() or shift == 0:
            return self
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
        exp = other.copy()
        a = self.copy()
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
        exp = exponent.copy()
        a = self.copy()
        res = bigint.one()
        c = 0
        while exp > bigint.zero():
            if exp.num[0] == 1:
                res = (res * a) % module
                exp -= bigint.one()
            else:
                a = (a * a) % module
                exp >> 1
            c += 1
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

# a = bigint.from_dec(
#     20282408047797612116049925965414144851286952783273771973)
# b = bigint.from_dec(20282408092494394779761211604992)

# a = bigint.from_dec(434)
# b = bigint.from_dec(13)

# print "a: {}".format(a)
# print "b: {}".format(b)


# start = time.time()
# res = copy.deepcopy(a)
# for i in range(0, 10):
#     res << 2
#     res.long_division(b)
# res = a.long_division(b)
# print "{} = {} * {} + {}\nlong time: {}s".format(a, res[0], b, res[1], time.time() - start)

# start = time.time()
# res = copy.deepcopy(a)
# for i in range(0, 10):
#     res << 2
#     res.division(b)
# res = a.division(b)
# print "{} = {} * {} + {}\ndef time: {}s".format(a, res[0], b, res[1], time.time() - start)


# start = time.time()
# res = copy.deepcopy(a)
# for i in range(0, 100):
#     res << 2
#     a - b
# res = a - b
# print "{} = {} - {}\nlong time: {}s".format(res, a, b, time.time() - start)

# import time
# a = bigint.from_dec(434)
# b = bigint.from_dec(13)

# print "a: {}".format(a)
# print "b: {}".format(b)

# start = time.time()
# res = copy.deepcopy(a)
# for i in range(0, 10):
#     res << 2
#     res.long_division(b)
# res = a.long_division(b)
# print "{} = {} * {} + {}\nlong time: {}s".format(a, res[0], b, res[1], time.time() - start)
