import math
import random
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


def introot(z, n):
    y = 0
    b = z.bit_length()
    for i in reversed(range(b)):
        x = 2**i
        y_ = y + x
        if y_ ** n <= z:
            y = y_
    return y


def modpow(x, n, z):
    if n <= 0:
        return 1 % z
    if n <= 1:
        return x % z
    if n % 2 == 0:
        t = modpow(x, n >> 1, z)
        return (t * t) % z
    return (x * modpow(x, n - 1, z)) % z


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


def mrtest(z, rounds=512):
    """Miller-Rabin test"""
    if z == 2:
        return True
    if z == 3:
        return True
    d = z-1
    s = 0
    while d % 2 == 0:
        s += 1
        d >>= 1
    while rounds:
        rounds -= 1
        a = random.randint(2, z-1)
        p = modpow(a, d, z)
        for _ in range(s):
            p_ = modpow(p, 2, z)
            if p_ == 1 and p != 1 and p != z-1:
                return False
            p = p_
        if p != 1:
            return False
    return True


def rec(z):
    if mrtest(z):
        return
    if z % 2 == 0:
        return 2
    if z % 3 == 0:
        return 3
    r = intsqrt(z)
    if r**2 == z:
        return r
    print()

    def inner(m=1):
        global counter
        nonlocal z
        counter += 1
        if counter % 100 == 0:
            print("\x1bM\x1b[2K", end="\r")
            print(counter, m)
        g = math.gcd(z, m % z)
        if 1 < g < z:
            return g
        for i in range(0, int(math.log2(z.bit_length()))*z.bit_length()):
            m_ = m + modpow(2, i, z)
            g = math.gcd(z, m_)
            if 1 < g < z:
                return g
            m_ = -m + modpow(2, i, z)
            g = math.gcd(z, abs(m_ % z))
            if 1 < g < z:
                return g
        for i in reversed(range(max_bit(m)+1, intsqrt(z).bit_length()+1)):
            if not (m & (1 << i)):
                m_ = m | (1 << i)
                if z // m_**1 >= m_**1:
                    if r := inner(m_):
                        return r
    return inner()


def factr(z):
    r = rec(z)
    g = r or 1
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
                        f[e] += j*v
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
    import sys
    sys.setrecursionlimit(10000)

    random.seed(1)
    max_bits = 256
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
    # a = 2**521-1
    # b = 2**189-1
    c = a * b
    if True:
        print(a.bit_length(), "×", b.bit_length(), "=", c.bit_length(), "(bits)")
        print(c)
        counter = 0
        f = factr(c)
        print()
        print(counter)
        print(f, False if not f else tuple(((1 < p < c) and c % (p**v) == 0,
              p.bit_length()) for p, v in f.items()))

    C = 0
    B = 0
    n = 0
    m = math.inf
    M = 0
    G = set()
    F = set()
    try:
        # for a, b in [(5, 5), (3, 3), (11, 13), (613, 997), (6857, 7793), (86028121, 15485863)]:
        # for a, b in [(261, 373), (613, 997), (6857, 7793), (9037105942710489806344254367233541671331400809491838136340060908904658662351543450913, 1766847066423888886904503541470640004349646523777212942116503594152755201)]:
        # for a, b in [(5, 5), (3, 3), (11, 13), (613, 997), (6857, 7793)]:
        # for a, b in [(5, 5), (3, 3), (11, 13), (13, 17), (19, 23), (41, 73), (43, 79)]:
        # for a, b in [(5, 5), (3, 3), (11, 13), (13, 17), (19, 23), (41, 73), (43, 79)]:
        # for a, b in [(15193, 19777), (15217, 19949)]:
        # for a, b in [(127, 141)]:
        # for a, b in [(6967677979, 6967677973)]:
        # for a, b in [(7919, 5987)]:
        for a in range(2, 1000):
            a = a + 100000000
            if not mrtest(a):
                continue
            for b in range(a+1000000000, a+1000001000):
                if not mrtest(b):
                    continue
                counter = 0
                c = a*b
                f = factr(c)
                F = F.union(f.keys())
                n += 1
                C += counter
                B += c.bit_length()
                m = min(m, counter)
                if counter > M:
                    G.add((counter, a, b, c))
                M = max(M, counter)
                if not f:
                    print("\n", a, b)
                    print(c.bit_length(), counter)
                    raise ValueError
                print(counter)
                break
    finally:
        print(n, C, C / n, B, B / n, M, m)
        print(max(G, key=lambda g: g[0]))
