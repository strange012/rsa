from functools import reduce
from conventer import bin_to_dec, dec_to_bin
import copy


def myprint(mylist):
    print [str(x) for x in mylist]


class bigint:
    num = []

    def __init__(self, num):
        self.num = list(num)
        self.num.reverse()

    def get_reversed(self):
        return bigint(self.num)

    @classmethod
    def one(cls):
        return cls([1])

    @classmethod
    def zero(cls):
        return cls([0])

    @classmethod
    def from_str(cls, s):
        return cls([int(x) for x in s])

    @classmethod
    def from_dec(cls, dec):
        return cls.from_str(dec_to_bin(dec))

    def __len__(self):
        return len(self.num)

    def __str__(self):
        return reduce((lambda x, y: str(y) + x), self.num, "")

    def __add__(self, other):
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
        return bigint(res).get_reversed()

    def __sub__(self, other):
        carry = 0
        i = 0
        a = copy.deepcopy(self)
        while i in range(0, len(a.num)) or carry:
            a.num[i] -= (other.num[i] if i < len(other.num) else 0) + carry
            carry = a.num[i] < 0
            a.num[i] = a.num[i] % 2
            i += 1
        while ((len(a.num) > 1) and (a.num[-1] == 0)):
            a.num.pop()
        return a

    def __eq__(self, other):
        return self.num == other.num

    def __lt__(self, other):
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
        a = copy.deepcopy(self)
        b = copy.deepcopy(other)
        b << (len(a) - len(b))
        quot = []

        while len(b) >= len(other):
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
            return bigint.zero()
        self.num = self.num[shift:]
        return self

    def __pow__(self, other):
        exp = copy.deepcopy(other)
        a = copy.deepcopy(self)
        res = bigint([1])
        while exp > bigint.zero():
            if exp.num[0] == 1:
                res *= a
                exp -= bigint.one()
            else:
                a *= a
                exp >> 1
        return res

    def mod_pow(self, exponent, module):
        exp = copy.deepcopy(exponent)
        a = copy.deepcopy(self)
        res = bigint([1])
        while exp > bigint.zero():
            if exp.num[0] == 1:
                res = (res * a) % module
                exp -= bigint.one()
            else:
                a = (a * a) % module
                exp >> 1
        return res


long1 = "100111110101000010010000001001000010101011100010001100\
110101100110010001110110011001010100110001100010000000100101100\
101110010111101110001001001100111000011000111101100000111010101\
00000011000000010010001100010010101"

long2 = "100001111100001010010110111011010100100000001111100110\
101011000101111000100001011101111011001101001100010001100101111\
101011000010111011101111001110000001101101011000111000011000011\
00100011010010011001011011100001"

p = bigint.from_str(long1)
q = bigint.from_str(long2)

n = p * q

f = (p - bigint.one()) * (q - bigint.one())
# print(n)


# print "c = a / b: {}".format(a / b)


import time

a = bigint.from_dec(57)
p = bigint.from_dec(239)

exp = p - bigint.one()
print "a: {}".format(a)
print "p: {}".format(p)
print "p-1: {}".format(exp)

start = time.time()
res = a**exp
print "a**p-1: {}\n{}s".format(res, time.time() - start)

# start = time.time()
# t = res / p
# print "a**exp / p: {}\n{}s".format(t, time.time() - start)

start = time.time()
t = a.mod_pow(exp, p)
print "a**p-1 mod p (mod pow): {}\n{}s".format(t,  time.time() - start)
