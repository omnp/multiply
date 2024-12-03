import math
import multiplication3 as m3


def intsqrt(z):
    y = 0
    b = z.bit_length()
    for i in reversed(range(b)):
        x = 2**i
        y_ = y + x
        if y_ * y_ <= z:
            y = y_
    return y


def min_bit(z):
    p_ = z
    k_ = 0
    k = 0
    while p_:
        if p_ & 1:
            k_ = k
            break
        k += 1
        p_ >>= 1
    return k_


def max_bit(z):
    p_ = z
    k_ = 0
    k = 0
    while p_:
        if p_ & 1:
            k_ = k
        k += 1
        p_ >>= 1
    return k_


def rec(z):
    global counter
    b = z.bit_length()-1
    y = 1
    ys = [y]
    T = z
    while ys:
        #  y = ys.pop()
        y = min(ys)
        ys.remove(y)
        g = math.gcd(z, y)
        if 1 < g < z:
            return g
        i = 1
        m = b-1-(min_bit(y>>1))
        t = z
        ys_ = []
        while i < m:
            counter += 1
            x = 2**(i)
            y_ = y + x
            w = z // y_
            g = math.gcd(z, y_)
            if 1 < g < z:
                return g
            if 2 <= y_ < z and 2 <= w < z:
                if z - y_ * w < t:
                    t = z - y_ * w
                    if t < T:
                        T = t
                        ys.clear()
                    ys_.clear()
                    if y_ not in ys:
                        assert y_ not in ys_
                        assert y_ > y
                        ys_.append(y_)
            i += 1
        ys.extend(ys_)


def factr(z):
    g = 1
    r = rec(z)
    if r is not None:
        g = r
    print(f"Found factor: {g}")
    f = {}
    if 1 < g < z:
        gs = [g]
        for g in gs:
            if 1 < g < z:
                j = 0
                while z % g == 0:
                    j += 1
                    z = z // g
                h = factr(g)
                if h:
                    for e, v in h.items():
                        if e not in f:
                            f[e] = 0
                        f[e] += v
                else:
                    if g not in f:
                        f[g] = 0
                    f[g] += j
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


counter = 0


if __name__ == '__main__':

    import random

    random.seed(1)
    max_bits = 16
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
    # a = 2**a-1-2**(a//2)
    # b = 2**b-1-2**(b//2)
    a = 2**521-1
    b = 2**127-1
    c = a * b
    print(a.bit_length(), "×", b.bit_length(), "=", c.bit_length(), "(bits)")
    counter = 0
    f = factr(c)
    print(counter)
    print(f, False if not f else tuple(((1 < p < c) and c % (p**v) == 0,
          p.bit_length()) for p, v in f.items()))

    # for a, b in [(11, 13), (13, 17), (261, 373), (2**261-1, 2**373-1),
    #              (2**(2**13-1)-1, 2**(2**11-1)-1)]:
    # for a, b in [(5, 5), (3, 3), (613, 997), (6857, 7793), (86028121, 15485863)]:
    # for a, b in [(261, 373), (613, 997), (6857, 7793), (9037105942710489806344254367233541671331400809491838136340060908904658662351543450913, 1766847066423888886904503541470640004349646523777212942116503594152755201)]:
    for a, b in [(5, 5), (3, 3), (11, 13), (13, 17), (41, 73), (43, 79)]:
        counter = 0
        c = a*b
        f = factr(c)
        print(f, False if not f else tuple((1 < p < c) and c % (p**v) == 0 for
                                           p, v in f.items()))
        print(c.bit_length(), counter)
