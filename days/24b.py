from copy import copy
DIRECTIONS = ['e', 'w', 'se', 'sw', 'nw', 'ne']


def get_direction(tile_id):
    if tile_id[0] in ['e', 'w']:
        return tile_id[0]
    return tile_id[:2]


def flip_tile(tile):
    new_color = 'b' if tile['color'] == 'w' else 'w'
    tile['color'] = new_color
    return tile


def get_new_coord(coord, direction):
    x, y = coord
    new_x, new_y = x, y
    if direction == 'e':
        new_x = x + 2
    elif direction == 'w':
        new_x = x - 2
    elif direction == 'se':
        new_x = x + 1
        new_y = y + 1
    elif direction == 'sw':
        new_x = x - 1
        new_y = y + 1
    elif direction == 'nw':
        new_x = x - 1
        new_y = y - 1
    elif direction == 'ne':
        new_x = x + 1
        new_y = y - 1
    return new_x, new_y


def process_tile_id(tile_id, tiling):
    i = 0
    coord = (0, 0)
    while i < len(tile_id):
        direction = get_direction(tile_id[i:])
        coord = get_new_coord(coord, direction)

        i += len(direction)
    if coord not in tiling:
        tiling[coord] = 'w'
    tiling[coord] = 'b' if tiling[coord] == 'w' else 'w'

    return tiling


def get_neighbors(coord):
    return list([get_new_coord(coord, d) for d in DIRECTIONS])


with open('input/24.txt') as f:
    tile_ids = [l.strip() for l in f.readlines()]
    tiling = {(0, 0): 'w'}
    for tile_id in tile_ids:
        tiling = process_tile_id(tile_id, tiling)
    blacks = [coord for coord, c in tiling.items() if c == 'b']
    n_blacks = len(blacks)

    for day in range(1, 101):
        if day % 10 == 0:
            print('Iteration', day, len(tiling))
        new_tiling = copy(tiling)
        blacks = [coord for coord, c in tiling.items() if c == 'b']
        coords = copy(blacks)
        visited = set([])
        while len(coords) > 0:
            coord = coords.pop()
            visited.add(coord)

            if coord not in tiling:
                color = 'w'
            else:
                color = tiling[coord]
            neighbors = get_neighbors(coord)

            n_black_neighbors = len(
                [n for n in neighbors if n in tiling and tiling[n] == 'b'])
            if color == 'b':
                for n in neighbors:
                    if n not in visited:
                        coords.append(n)
                if n_black_neighbors == 0 or n_black_neighbors > 2:
                    new_tiling[coord] = 'w'
            if color == 'w' and n_black_neighbors == 2:
                new_tiling[coord] = 'b'
        tiling = new_tiling

    blacks = [coord for coord, c in tiling.items() if c == 'b']
    n_blacks = len(blacks)
    print(n_blacks)
