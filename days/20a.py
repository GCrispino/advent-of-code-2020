import numpy as np


def parse_tile_strs(tile_strs):
    tiles = {}
    for tile_str in tile_strs:
        lines = tile_str.split('\n')
        tile_id = int(lines[0].split(' ')[1][:-1])
        tile_body = np.array(
            [np.where(np.array(list(l)) == '#', 1, 0) for l in lines[1:]], dtype=np.uint8)
        tiles[tile_id] = tile_body
    return tiles


def find_matches(tile_id, checksums):
    tile_checksums = checksums[tile_id]
    matches = []
    for _id, _checksums in checksums.items():
        if _id == tile_id:
            continue
        matched = False
        for (c1, c2) in tile_checksums:
            if matched:
                break
            for (_c1, _c2) in _checksums:
                match = (c1 == _c1) or (c1 == _c2) or (
                    c2 == _c1) or (c2 == _c2)
                if match:
                    matches.append(_id)
                    matched = True
                    break
    return matches


with open('input/20.txt') as f:
    tile_strs = f.read().strip().split('\n\n')
    tiles = parse_tile_strs(tile_strs)
    arange = 2 ** np.arange(0, next(iter(tiles.values())).shape[0])
    checksums = {}
    for tile_id, tile in tiles.items():
        checksums[tile_id] = [(tile[0].dot(arange), tile[0][::-1].dot(arange)),
                              (tile[:, -1].dot(arange),
                               tile[:, -1][::-1].dot(arange)),
                              (tile[-1].dot(arange),
                               tile[-1][::-1].dot(arange)),
                              (tile[:, 0].dot(arange), tile[:, 0][::-1].dot(arange))]

    matches = {}
    for tile_id in tiles:
        matches[tile_id] = find_matches(tile_id, checksums)

    res = 1
    for tile_id, m in matches.items():
        if len(m) == 2:
            res *= tile_id

    print(res)
