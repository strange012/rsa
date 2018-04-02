from functools import reduce

class bigint:
    num = []

    def __init__(self, num):
        self.num = num
        self.num.reverse()

    def to_str(self):
        return reduce((lambda x,y : str(y) + str(x)), self.num)

    def __add__(self, other):
        carry = 0
        for i in range(0, max(len(self.num), len(other.num))):
            if (i == len(self.num)):
                self.num.append(0)
            
            self.num[i] = carry + self.num[i] + (other.num[i] if i < len(other.num) else 0)
            carry = self.num[i] / 2
            self.num[i] = self.num[i] % 2
        if carry:
            self.num.append(carry)
        return self

    def __mul__(self, other):
        res = [0]*(len(self.num) + len(other.num))
        for i in range(0, len(self.num)):
            for j in range(0, len(other.num)):
                res[i+j] += self.num[i]*other.num[j]
        for i in range(0, len(self.num) + len(other.num) - 1):
            res[i+1] += res[i] / 2
            res[i] = res[i] % 2
        while ((len(res) > 1) and (res[-1] == 0)):
            res.pop()
        return bigint(res).get_reversed()

    def __sub__(self, other):
        carry = 0
        i = 0
        while (i in range(0, len(self.num)) and (i < len(other.num) or carry)):
            self.num[i] -= (other.num[i] if i < len(other.num) else 0) + carry
            carry = 0 if self.num[i] >= 0 else 1
            self.num[i] = self.num[i] % 2
            i += 1
        while ((len(self.num) > 1) and (self.num[-1] == 0)):
            self.num.pop()
        return self

    def division(self, other):
        

    def get_reversed(self):
        return bigint(self.num)


def str_to_list(s):
    return [int(x) for x in s]

astr = "1101110"
bstr = "1110100100111"
a = bigint(str_to_list(astr))
b = bigint(str_to_list(bstr))
print((a*b).to_str())


cstr = "110101010101"
dstr = "1101001"
c = bigint(str_to_list(cstr))
d = bigint(str_to_list(dstr))
print((c - d).to_str())

