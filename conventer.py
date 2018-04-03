def dec_to_bin(num):
    return bin(num)[2:] if num >= 0 else "-" + bin(num)[3:]


def bin_to_dec(s):
    return int(s, 2)
