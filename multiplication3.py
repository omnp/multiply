def sign(n):
    return int(n > 0) - int(n < 0)
    

def transform_integer(n: int) -> [int]:
    powers = []
    k = 0
    while n:
        if n & 1:
            powers.append(k)
        n >>= 1
        k += 1
    return powers


def inverse_integer(powers: [int]) -> int:
    return sum(2**e for e in powers)


def multiply(a: dict[int, int|float|complex], b: dict[int, int|float|complex]) -> dict[int, int|float|complex]:
    terms = {}
    for e, u in a.items():
        for f, v in b.items():
            w = u*v
            if w != 0:
                if e+f not in terms:
                    terms[e + f] = 0
                terms[e + f] += w
    return normalize(terms)


def add(a: dict[int, int|float|complex], b: dict[int, int|float|complex]) -> dict[int, int|float|complex]:
    terms = {}
    for e, v in a.items():
        if e not in terms:
            terms[e] = 0
        terms[e] += v
    for f, v in b.items():
        if f not in terms:
            terms[f] = 0
        terms[f] += v
    for g, w in list(terms.items()):
        if w == 0:
            del terms[g]
    return normalize(terms)


def sub(a: dict[int, int|float|complex], b: dict[int, int|float|complex]) -> dict[int, int|float|complex]:
    terms = {}
    for e, v in a.items():
        if e not in terms:
            terms[e] = 0
        terms[e] += v
    for f, v in b.items():
        if f not in terms:
            terms[f] = 0
        terms[f] -= v
    for g, w in list(terms.items()):
        if w == 0:
            del terms[g]
    return normalize(terms)


def normalize(terms: dict[int, int|float|complex], modulo = lambda n: n % 2, not_zero = lambda n: n != 0, sign = lambda n: int(n > 0) - int(n < 0), shift = lambda n: n >> 1) -> dict[int, int|float|complex]:
    keys = list(sorted(terms.keys()))
    while keys:
        e = min(keys)
        keys.remove(e)
        n = terms[e]
        if not keys and n < 0:
            break
        del terms[e]
        if not_zero(modulo(n)):
            terms[e] = modulo(n)
            n = n - terms[e]
        n = shift(n)
        if not_zero(n):
            if e+1 not in terms:
                terms[e+1] = 0
                keys.append(e+1)
            terms[e+1] += n
    return terms


def transform(n: int) -> dict[int, int|float|complex]:
    if isinstance(n, dict):
        return normalize(dict(n))
    s = 1
    if isinstance(n, list):
        nt = n
    else:
        s = sign(n)
        nt = transform_integer(abs(n))
    return {e: s for e in nt}


def inverse(powers: dict[int, int|float|complex]) -> int|float|complex:
    return sum(v * 2**e for e, v in powers.items())


def multiply_recursive(a: dict[int, int|float|complex], b: dict[int, int|float|complex], K: int = 4, recursive: bool = False) -> dict[int, int|float|complex]:
    """
    Multiply (recursively) together two values. Using the Karatsuba method.
    """
    global recursion_counter
    recursion_counter += 1
    a = transform(a)
    b = transform(b)
    if len(a) >= K and len(b) >= K:
        n = min(max(a.keys()), max(b.keys()))
        n >>= 1
        a_high = {e: u for e, u in a.items() if e >= n}
        b_high = {f: v for f, v in b.items() if f >= n}
        a_low = sub(a, a_high)
        b_low = sub(b, b_high)
        a_high = {e-n: u for e, u in a_high.items()}
        b_high = {f-n: v for f, v in b_high.items()}
        c_high = multiply_recursive(a_high, b_high, K=K, recursive=True)
        c_low = multiply_recursive(a_low, b_low, K=K, recursive=True)
        c_mid = multiply_recursive(add(a_high, a_low), add(b_high, b_low), K=K, recursive=True)
        c_mid = sub(c_mid, add(c_high, c_low))
        c_high = {g + 2*n: w for g, w in c_high.items()}
        c_mid = {g + n: w for g, w in c_mid.items()}
        c = add(c_high, add(c_mid, c_low))
    else:
        c = multiply(a, b)
    return normalize(c)


def multiply_integers(a, b, K=4):
    at = transform(a)
    bt = transform(b)
    ct = multiply_recursive(at, bt, K)
    c = inverse(ct)
    return c


recursion_counter = 0

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(100000)

    for a, b in [(11, 13), (13, 17), (261, 373), (2**261-1, 2**373-1),#]:
                 (2**(2**13-1)-1, 2**(2**11-1)-1)]:
        print(a.bit_length(), b.bit_length())
        at, bt = transform(a), transform(b)
        c = inverse(add(at, bt))
        print(a, "+", b, "=", c, c == a+b)
        c = inverse(sub(at, bt))
        print(a, "-", b, "=", c, c == a-b)
        recursion_counter = 0
        c = multiply_integers(a, b, K=4)
        print(a, "*", b, "=", c)
        print(c == a*b)
        print(c.bit_length())
        print(recursion_counter)
