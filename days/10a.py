import numpy as np

with open('input/10-test.txt') as f:
    ns = np.array([0] + sorted(map(int, f.readlines())))
    diffs = np.concatenate([ns[1:], [0]]) - ns
    n_1 = np.sum(diffs == 1)
    n_3 = np.sum(diffs == 3) + 1
    print(n_1 * n_3)
