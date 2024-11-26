import math
import multiplication3 as m3


def factr(z):
    zt = m3.transform(z)
    k = max(zt.keys())
    for n in range(k):
        zt_ = dict(zt)
        for i in reversed(range(1, k+1)):
            t = zt_[i]
            if i > n:
                del zt_[i]
                if i-1 not in zt_:
                    zt_[i-1] = 0
                zt_[i-1] += 2*t
            else:
                zt_[i] = 1
                t -= 1
                if i-1 not in zt_:
                    zt_[i-1] = 0
                zt_[i-1] += 2*t
            g = math.gcd(z, zt_[i-1])
            if 1 < g < z:
                z = z // g
                f = {}
                h = factr(g)
                if h:
                    for e, v in h.items():
                        if e not in f:
                            f[e] = 0
                        f[e] += v
                else:
                    if g not in f:
                        f[g] = 0
                    f[g] += 1
                if 1 < z:
                    h = factr(z)
                    if h:
                        for e, v in h.items():
                            if e not in f:
                                f[e] = 0
                            f[e] += v
                    else:
                        if z not in f:
                            f[z] = 0
                        f[z] += 1
                return f
    return {}


if __name__ == '__main__':

    import random

    max_bits = 2048
    a_bits = random.randint(max_bits >> 1, max_bits)
    b_bits = random.randint(max_bits >> 1, max_bits)

    a = {}
    a[0] = 1
    a[a_bits] = 1
    for i in range(2, a_bits):
        if random.choice((True, False)):
            a[i] = 1
    b = {}
    b[0] = 1
    b[b_bits] = 1
    for i in range(2, b_bits):
        if random.choice((True, False)):
            b[i] = 1
    a = m3.inverse(a)
    b = m3.inverse(b)
    c = a * b
    print(a.bit_length(), "×", b.bit_length(), "=", c.bit_length(), "(bits)")
    f = factr(c)
    print(f, False if not f else tuple((1 < p < c) and c % (p**v) == 0 for
                                       p, v in f.items()))

    """
    for a, b in [(11, 13), (13, 17), (261, 373), (2**261-1, 2**373-1),
                 (2**(2**13-1)-1, 2**(2**11-1)-1)]:
        c = a*b
        f = factr(c)
        print(f, False if not f else tuple((1 < p < c) and c % (p**v) == 0 for
                                           p, v in f.items()))
        print(c.bit_length())
    """
