from math import prod


def get_n_trees(path_map, slope=(3, 1)):
    x = 0
    y = 0
    slope_x, slope_y = slope
    y_max = len(path_map) - 1
    trees_found = 0
    traversal = []
    while y <= y_max:
        x_max = len(path_map[y])

        found = False
        if path_map[y][x] == 1:
            found = True
            trees_found += 1
        mark = 'O' if not found else 'X'
        traversal.append(''.join([mark if i == x else (
            '#' if x_ == 1 else '.') for (i, x_) in enumerate(path_map[y])]))
        x = x + slope_x if x + slope_x < x_max else x + slope_x - x_max
        y += slope_y
    return trees_found, '\n'.join(traversal)


slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

with open('input/3.txt') as f:
    lines = f.readlines()
    path_map = [[1 if c == '#' else 0 for c in l[:-1]] for l in lines]
    res = prod([get_n_trees(path_map, slope)[0] for slope in slopes])
    print(res)
