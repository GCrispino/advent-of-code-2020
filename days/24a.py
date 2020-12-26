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


with open('input/24.txt') as f:
    tile_ids = [l.strip() for l in f.readlines()]
    tiling = {(0, 0): 'w'}
    for tile_id in tile_ids:
        tiling = process_tile_id(tile_id, tiling)
    n_blacks = sum([1 for c in tiling.values() if c == 'b'])
    print(n_blacks)
