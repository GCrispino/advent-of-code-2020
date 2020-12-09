import numpy as np


def find_contiguous_set(ns, invalid):
    start = 0
    end = 1

    while start < len(ns) - 1:
        contiguous = ns[start:end + 1]
        sum_contiguous = sum(contiguous)
        if sum_contiguous == invalid:
            return contiguous
        if sum_contiguous > invalid:
            start += 1
            end = start + 1
        else:
            end += 1


with open('input/9.txt') as f:
    pre_size = 25
    ns = list(map(int, f.readlines()))
    invalid = find_invalid_number(ns, pre_size)
    contiguous_set = find_contiguous_set(ns, invalid)
    sorted_set = sorted(contiguous_set)

    print(sorted_set[0] + sorted_set[-1])
