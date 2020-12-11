import numpy as np


def get_n_arrangements_from(start, ns, memo=None):
    memo = {} if memo == None else memo
    if start == len(ns) - 1:
        return 1

    n = ns[start]

    next_possible = []
    i = start + 1
    while i < len(ns) and ns[i] - n <= 3:
        next_possible.append(i)
        i += 1
    n_arrangements = 0
    for nxt in next_possible:
        if nxt in memo:
            n_arrangements_ = memo[nxt]
        else:
            n_arrangements_ = get_n_arrangements_from(nxt, ns, memo)
            memo[nxt] = n_arrangements_
        n_arrangements += n_arrangements_
    return n_arrangements


with open('input/10.txt') as f:
    ns = np.array([0] + sorted(map(int, f.readlines())))
    n_arrangements = get_n_arrangements_from(0, ns)

    print(n_arrangements)
