def multiply(a, b, memory=None):
    """ Multiply two (big) integers together recursively.
        Quite a memory hungry procedure. """
    
    global counter
    counter += 1

    if memory is None:
        memory = {}

    def split(a):
        n = a.bit_length()
        if n > 1:
            n = n >> 1
            beg = a >> n
            end = a - (beg << n)
            return beg, end, n
        return a, 0, 0

    beg, end, offset = split(a)
    if beg not in memory:
        if abs(beg) > 1:
            memory[beg] = multiply(beg, b, memory)
        else:
            memory[beg] = beg * b
    if end not in memory:
        if abs(end) > 1:
            memory[end] = multiply(end, b, memory)
        else:
            memory[end] = end * b
    return (memory[beg] << offset) + memory[end]

counter = 0
