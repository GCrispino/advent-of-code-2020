def get_neighbors(x, y, z):
    neighbors = []
    for x_ in range(x - 1, x + 2):
        for y_ in range(y - 1, y + 2):
            for z_ in range(z - 1, z + 2):
                if (x_, y_, z_) == (x, y, z):
                    continue
                neighbors.append((x_, y_, z_))
    return neighbors


def get_alive_neighbors(x, y, z, neighbors, grid):
    alive = []
    for (x_, y_, z_) in neighbors:
        try:
            if grid[(x_, y_, z_)] == '#':
                alive.append((x_, y_, z_))
        except KeyError:
            pass
    return alive


with open('input/17.txt') as f:
    lines = [l.strip() for l in f.readlines()]
    dim_region = len(lines)
    grid = {}
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            grid[(x, y, 0)] = c

    for i in range(6):
        coords = grid.keys()
        x_coords = [c[0] for c in coords]
        y_coords = [c[1] for c in coords]
        z_coords = [c[2] for c in coords]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        z_min, z_max = min(z_coords), max(z_coords)

        changes = []
        for z in range(z_min - 1, z_max + 2):
            for y in range(y_min - 1, y_max + 2):
                for x in range(x_min - 1, x_max + 2):
                    neighbors = get_neighbors(x, y, z)
                    alive = get_alive_neighbors(x, y, z, neighbors, grid)
                    n_alive = len(alive)
                    cube_value = None
                    try:
                        cube_value = grid[(x, y, z)]
                    except:
                        cube_value = '.'
                    if cube_value == '.' and n_alive == 3:
                        changes.append(((x, y, z), '#'))
                    if cube_value == '#' and (n_alive != 2 and n_alive != 3):
                        changes.append(((x, y, z), '.'))

        for coord, new_value in changes:
            grid[coord] = new_value
    res = sum([1 for c in grid.values() if c == '#'])
    print(res)
