import numpy as np

neighbour_func = {
    'N': lambda i, j: (i - 1, j),
    'S': lambda i, j: (i + 1, j),
    'W': lambda i, j: (i, j - 1),
    'E': lambda i, j: (i, j + 1),
    'NW': lambda i, j: (i - 1, j - 1),
    'NE': lambda i, j: (i - 1, j + 1),
    'SW': lambda i, j: (i + 1, j - 1),
    'SE': lambda i, j: (i + 1, j + 1)
}


def get_neighbour(i, j, n_id, seat_map):

    i_, j_ = i, j
    while True:
        i_, j_ = neighbour_func[n_id](i_, j_)
        if i_ < 0 or i_ >= seat_map.shape[0] or j_ < 0 or j_ >= seat_map.shape[1]:
            return None
        if seat_map[i_, j_] != '.':
            return seat_map[i_, j_]
    return None


def get_neighbours(i, j, n_ids, seat_map):
    return [get_neighbour(i, j, n_id, seat_map) for n_id in n_ids]


def compute_new_seat(i, j, seat_map):
    if seat_map[i, j] == '.':
        return seat_map[i, j]
    neighbours = get_neighbours(i, j, neighbour_func.keys(), seat_map)
    n_occupied = sum([1 for i in neighbours if i == '#'])
    if seat_map[i, j] == 'L' and n_occupied == 0:
        return '#'

    if seat_map[i, j] == '#' and n_occupied >= 5:
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
