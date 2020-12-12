import numpy as np


def compute_new_seat(i, j, seat_map):
    if seat_map[i, j] == '.':
        return seat_map[i, j]
    above = [] \
        if i == 0 \
        else seat_map[
            i - 1, max(j - 1, 0):min(j + 2, seat_map.shape[1])].tolist()
    row = seat_map[i, [*([] if j == 0 else [j - 1]), *
                       ([] if j == seat_map.shape[1] - 1 else [j + 1])]].tolist()
    below = [] \
        if i == seat_map.shape[0] - 1 \
        else seat_map[
            i + 1, max(j - 1, 0):min(j + 2, seat_map.shape[1])].tolist()
    neighbours = above + row + below
    n_occupied = sum([1 for i in neighbours if i == '#'])
    if seat_map[i, j] == 'L' and n_occupied == 0:
        return '#'

    if seat_map[i, j] == '#' and n_occupied >= 4:
        return 'L'
    return seat_map[i, j]


with open('input/11.txt') as f:
    seat_map = np.array([list(l.strip()) for l in f.readlines()])

    k = 0
    while True:
        new_seat_map = np.array(seat_map)
        changed = False
        for i, row in enumerate(seat_map):
            for j, seat in enumerate(row):
                new_seat = compute_new_seat(i, j, seat_map)
                new_seat_map[i, j] = new_seat
                if not changed and new_seat != seat:
                    changed = True
        seat_map = new_seat_map
        if not changed:
            break
        if k % 10 == 0:
            print("Iteration", k)
        k += 1
    print(np.sum(seat_map == '#'))
