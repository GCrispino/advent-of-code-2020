import numpy as np


def find_invalid_number(ns, pre_size):
    rest = ns[pre_size:]

    for i, r in enumerate(rest):
        preamble = np.array(ns[i:i + pre_size])
        p_set = set(preamble)
        is_sum = False
        for p in r - preamble:
            if p in p_set:
                is_sum = True
                break
        if not is_sum:
            return r

    return None


with open('input/9.txt') as f:
    pre_size = 25
    ns = list(map(int, f.readlines()))
    res = find_invalid_number(ns, pre_size)
    print(res)
