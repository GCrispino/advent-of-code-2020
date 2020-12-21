def get_neighbors(x, y, z, w):
    neighbors = []
    for x_ in range(x - 1, x + 2):
        for y_ in range(y - 1, y + 2):
            for z_ in range(z - 1, z + 2):
                for w_ in range(w - 1, w + 2):
                    if (x_, y_, z_, w_) == (x, y, z, w):
                        continue
                    neighbors.append((x_, y_, z_, w_))
    return neighbors


def get_alive_neighbors(x, y, z, w, neighbors, grid):
    alive = []
    for (x_, y_, z_, w_) in neighbors:
        try:
            if grid[(x_, y_, z_, w_)] == '#':
                alive.append((x_, y_, z_, w_))
        except KeyError:
            pass
    return alive


with open('input/17.txt') as f:
    lines = [l.strip() for l in f.readlines()]
    dim_region = len(lines)
    grid = {}
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            grid[(x, y, 0, 0)] = c

    for i in range(1, 7):
        print(f"Running cycle number {i}...")
        coords = grid.keys()
        x_coords = [c[0] for c in coords]
        y_coords = [c[1] for c in coords]
        z_coords = [c[2] for c in coords]
        w_coords = [c[3] for c in coords]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        z_min, z_max = min(z_coords), max(z_coords)
        w_min, w_max = min(w_coords), max(w_coords)

        changes = []
        for w in range(w_min - 1, w_max + 2):
            for z in range(z_min - 1, z_max + 2):
                for y in range(y_min - 1, y_max + 2):
                    for x in range(x_min - 1, x_max + 2):
                        neighbors = get_neighbors(x, y, z, w)
                        alive = get_alive_neighbors(
                            x, y, z, w, neighbors, grid)
                        n_alive = len(alive)
                        cube_value = None
                        try:
                            cube_value = grid[(x, y, z, w)]
                        except:
                            cube_value = '.'
                        if cube_value == '.' and n_alive == 3:
                            changes.append(((x, y, z, w), '#'))
                        if cube_value == '#' and (n_alive != 2 and n_alive != 3):
                            changes.append(((x, y, z, w), '.'))

        for coord, new_value in changes:
            grid[coord] = new_value
    a = len([((x, y, z, w), 1) for (x, y, z, w), v in grid.items()
             if w == 0 and z == 1 and v == '#'])
    res = sum([1 for c in grid.values() if c == '#'])
    print(res)
