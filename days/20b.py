import matplotlib.pyplot as plt
import numpy as np

PLOT = True


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


def get_neighbors(tile_id, tiles):
    return [_tile_id for _tile_id, _tile_matches in tiles.items() if tile_id in _tile_matches]


def fill_tiles_border_from_corner(tile, corner_position, all_tiles, filled_tiles, filled_tile_set, corner_fns, stack, border_axis=0):
    if tile not in filled_tile_set:
        pos = corner_fns[corner_position][border_axis](corner_position)
        cur_tile = tile
        while True:
            # repeat until corner is in neighbor set
            filled_tile_set.add(cur_tile)
            filled_tiles[pos] = cur_tile
            _neighbors = get_neighbors(cur_tile, all_tiles)
            valid_neighbors = [
                n for n in _neighbors if len(all_tiles[n]) == 3 and n not in filled_tile_set]
            corner_neighbors = [
                n for n in _neighbors if len(all_tiles[n]) == 2 and n not in filled_tile_set]

            pos = corner_fns[corner_position][border_axis](pos)
            for n in corner_neighbors:
                stack.append((n, pos))
            if len(valid_neighbors) == 0:
                break
            cur_tile = valid_neighbors[0]


def build_image(tiles, matches, checksums):
    sorted_matches = sorted(
        matches.items(), key=lambda x: len(x[1]))
    corners = {c_id: matches for c_id, matches in sorted_matches[:4]}
    rest_tiles = {c_id: tile_matches for c_id,
                  tile_matches in sorted_matches[4:]}
    all_tiles = {c_id: tile_matches for c_id,
                 tile_matches in sorted_matches}

    n_tiles = len(tiles)
    tile_shape = len(next(iter(tiles.values())))
    image_shape = np.sqrt(n_tiles).astype(int)
    shape = tile_shape * image_shape
    image = np.zeros((shape, shape), dtype=np.uint8)
    new_image = np.zeros((shape, shape), dtype=np.uint8)
    image2 = np.zeros((shape, shape), dtype=np.uint8)
    image_match = np.zeros((image_shape, image_shape, 2), dtype=int)
    filled_tiles = np.zeros((image_shape, image_shape), dtype=int)
    filled_tile_set = set([])

    corner_fns = {
        (0, 0): ((lambda x: (x[0], x[1] + 1)), ((lambda x: (x[0] + 1, x[1])))),
        (0, image_shape - 1): ((lambda x: (x[0], x[1] - 1)), ((lambda x: (x[0] + 1, x[1])))),
        (image_shape - 1, image_shape - 1): ((lambda x: (x[0], x[1] - 1)), ((lambda x: (x[0] - 1, x[1])))),
        (image_shape - 1, 0): ((lambda x: (x[0], x[1] + 1)), ((lambda x: (x[0] - 1, x[1])))),
    }

    # - Começa com os corners
    stack = [(next(iter(corners)), (0, 0))]
    while len(stack) > 0:
        corner, corner_position = stack.pop()
        filled_tiles[corner_position] = corner
        filled_tile_set.add(corner)

        neighbors = get_neighbors(corner, rest_tiles)
        first_neighbor, second_neighbor = neighbors[0], neighbors[1]
        if filled_tiles[corner_fns[corner_position][0](corner_position)] == second_neighbor:
            first_neighbor, second_neighbor = second_neighbor, first_neighbor

        # Fill in from first neighbor
        fill_tiles_border_from_corner(
            first_neighbor, corner_position, all_tiles, filled_tiles, filled_tile_set, corner_fns, stack, 0)
        fill_tiles_border_from_corner(second_neighbor, corner_position,
                                      all_tiles, filled_tiles, filled_tile_set, corner_fns, stack, 1)

    for i in range(1, image_shape - 1):
        tile1, tile2 = filled_tiles[i - 1, 1], filled_tiles[i, 0]
        cur_middle_tile = [tile for tile in rest_tiles if len(rest_tiles[tile]) == 4 and tile1 in rest_tiles[tile]
                           and tile2 in rest_tiles[tile] and tile not in corners][0]

        j = 1
        while True:
            filled_tiles[i, j] = cur_middle_tile
            filled_tile_set.add(cur_middle_tile)
            next_tile_candidates = [_neighbor for _neighbor in all_tiles[cur_middle_tile]
                                    if len(all_tiles[_neighbor]) == 4 and _neighbor not in filled_tile_set and cur_middle_tile in all_tiles[_neighbor] and filled_tiles[i - 1, j + 1] in all_tiles[_neighbor]]
            j += 1
            if len(next_tile_candidates) == 0:
                break
            cur_middle_tile = next_tile_candidates[0]

    for i, row in enumerate(filled_tiles):
        for j, tile in enumerate(row):
            if j < len(row) - 1:
                x_neighbor_tile = filled_tiles[i, j + 1]
            else:
                x_neighbor_tile = filled_tiles[i, j - 1]
            x_neighbor_tile_checksums = checksums[x_neighbor_tile]

            if i < len(filled_tiles) - 1:
                y_neighbor_tile = filled_tiles[i + 1, j]
            else:
                y_neighbor_tile = filled_tiles[i - 1, j]
            y_neighbor_tile_checksums = checksums[y_neighbor_tile]
            tile_checksums = checksums[tile]
            match_tile_x, match_tile_y = None, None
            i_match_tile_x, i_match_tile_y = None, None
            match_neighbor_x, match_neighbor_y = None, None
            i_match_neighbor_x, i_match_neighbor_y = None, None
            for i_tile_checksum, (tile_checksum_1, tile_checksum_2) in enumerate(tile_checksums):
                if not match_neighbor_x:
                    x_neighbor_tile_checksum_match = [(checksum, i) for i, checksum in enumerate(x_neighbor_tile_checksums) if tile_checksum_1 ==
                                                      checksum[0] or tile_checksum_1 == checksum[1] or tile_checksum_2 == checksum[0] or tile_checksum_2 == checksum[1]]
                    if len(x_neighbor_tile_checksum_match) > 0:
                        match_tile_x = (tile_checksum_1, tile_checksum_2)
                        i_match_tile_x = i_tile_checksum
                        match_neighbor_x, i_match_neighbor_x = x_neighbor_tile_checksum_match[0]
                if not match_neighbor_y:
                    y_neighbor_tile_checksum_match = [(checksum, i) for i, checksum in enumerate(y_neighbor_tile_checksums) if tile_checksum_1 ==
                                                      checksum[0] or tile_checksum_1 == checksum[1] or tile_checksum_2 == checksum[0] or tile_checksum_2 == checksum[1]]
                    if len(y_neighbor_tile_checksum_match) > 0:
                        match_tile_y = (tile_checksum_1, tile_checksum_2)
                        i_match_tile_y = i_tile_checksum
                        match_neighbor_y, i_match_neighbor_y = y_neighbor_tile_checksum_match[0]

            image_match[i, j] = (i_match_tile_y, i_match_tile_x)
            image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                  j:tile_shape * j + tile_shape] = tiles[filled_tiles[i, j]]
            new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                      j:tile_shape * j + tile_shape] = tiles[filled_tiles[i, j]]
            image2[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                   j:tile_shape * j + tile_shape] = tiles[filled_tiles[i, j]]
            if (j < len(filled_tiles) - 1 and i_match_tile_x == 3) or (j == len(filled_tiles) - 1 and i_match_tile_x == 1):  # east/west

                new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                          j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                                                                     j:tile_shape * j + tile_shape][:, ::-1]
            if (i < len(filled_tiles) - 1 and i_match_tile_y == 0) or (i == len(filled_tiles) - 1 and i_match_tile_y == 2):  # north/south
                new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                          j:tile_shape * j + tile_shape] = np.array(new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                                                                              j:tile_shape * j + tile_shape])[::-1, :]
            if i_match_tile_y == 3:
                new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                          j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape * j:tile_shape * j + tile_shape].T[::-1, :]
                if i_match_tile_x == 2 and match_tile_x == match_neighbor_x:
                    new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                              j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                                                                         j:tile_shape * j + tile_shape][:, ::-1]
                if i_match_tile_x == 0 and match_tile_x != match_neighbor_x:
                    new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                              j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                                                                         j:tile_shape * j + tile_shape][:, ::-1]
            if i_match_tile_y == 1:
                new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                          j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape * j:tile_shape * j + tile_shape].T[:, ::-1]

    for _ in range(1):
        for i in range(1, len(filled_tiles)):
            for j in range(len(filled_tiles[0])):
                if np.any(new_image[i * tile_shape, tile_shape * j:tile_shape * j + tile_shape] != new_image[i * tile_shape - 1, tile_shape * j:tile_shape * j + tile_shape]):
                    new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                              j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                                                                         j:tile_shape * j + tile_shape][:, ::-1]
        for i in range(len(filled_tiles)):
            for j in range(1, len(filled_tiles[0])):
                if np.any(new_image[i * tile_shape:i * tile_shape + tile_shape, tile_shape * j] != new_image[i * tile_shape:i * tile_shape + tile_shape, tile_shape * j - 1]):
                    new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                              j:tile_shape * j + tile_shape] = new_image[tile_shape * i:tile_shape * i + tile_shape, tile_shape *
                                                                         j:tile_shape * j + tile_shape][:, ::-1]

        # Manual hardcoded part (not proud of this)
        new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                  11:tile_shape * 11 + tile_shape] = new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                                                               11:tile_shape * 11 + tile_shape][::-1, :]
        new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                  10:tile_shape * 10 + tile_shape] = new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                                                               10:tile_shape * 10 + tile_shape][::-1, :]
        new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                  9:tile_shape * 9 + tile_shape] = new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                                                             9:tile_shape * 9 + tile_shape][:, ::-1]
        new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                  8:tile_shape * 8 + tile_shape] = new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                                                             8:tile_shape * 8 + tile_shape][:, ::-1]
        new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                  7:tile_shape * 7 + tile_shape] = new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                                                             7:tile_shape * 7 + tile_shape][::-1, ::-1]
        new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                  4:tile_shape * 4 + tile_shape] = new_image[tile_shape * 11:tile_shape * 11 + tile_shape, tile_shape *
                                                             4:tile_shape * 4 + tile_shape][::-1, :]
    for i in range(1, image_shape):
        new_image[i * tile_shape, :] *= 10
        new_image[i * tile_shape - 1, :] *= 10
        new_image[:, i * tile_shape] *= 10
        new_image[:, i * tile_shape - 1] *= 10
        image2[i * tile_shape, :] *= 10
        image2[i * tile_shape - 1, :] *= 10
        image2[:, i * tile_shape] *= 10
        image2[:, i * tile_shape - 1] *= 10
    max_val = np.max(new_image)
    new_image = np.where(new_image == max_val, 10, new_image)
    image2 = np.where(image2 == max_val, 10, image2)
    if PLOT:
        plt.figure(num="Aligned Image")
        plt.imshow(new_image)

    new_image = np.where(new_image > 1, 1, new_image)
    return new_image


def find_sea_monster(image, sea_monster_arr):
    rotations = [(image, image[:, ::-1])]
    matches = {}
    for i in range(1, 4):
        prev_rotation, _ = rotations[i - 1]
        rotations.append((prev_rotation.T[:, ::-1], prev_rotation.T))
        matches[i, 0] = []
        matches[i, 1] = []
    signature_sea_monster = np.sum(sea_monster_arr)
    for i_r, (r1, r2) in enumerate(rotations):
        for i in range(image.shape[0] - sea_monster_arr.shape[0]):
            for j in range(image.shape[1] - sea_monster_arr.shape[1]):
                r1_slice = r1[i:i + sea_monster_arr.shape[0],
                              j:j + sea_monster_arr.shape[1]]
                r2_slice = r2[i:i + sea_monster_arr.shape[0],
                              j:j + sea_monster_arr.shape[1]]
                if np.sum(sea_monster_arr * r1_slice) == signature_sea_monster:
                    matches[i_r, 0].append((i, j))
                if np.sum(sea_monster_arr * r2_slice) == signature_sea_monster:
                    matches[i_r, 1].append((i, j))
    return matches, rotations


with open('input/20.txt') as f:
    tile_strs = f.read().strip().split('\n\n')
    tiles = parse_tile_strs(tile_strs)
    tile_shape = next(iter(tiles.values())).shape[0]
    arange = 2 ** np.arange(0, tile_shape)
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
    image = build_image(tiles, matches, checksums)
    cropped_size = (tile_shape - 2) * (image.shape[0] // tile_shape)
    cropped_image = np.zeros((cropped_size, cropped_size), dtype=int)

    for i in range(image.shape[0] // tile_shape):
        for j in range(image.shape[0] // tile_shape):
            cropped_image[i * (tile_shape - 2):i * (tile_shape - 2) + (tile_shape - 2), j * (tile_shape - 2):j * (tile_shape - 2) +
                          (tile_shape - 2)] = image[i * tile_shape + 1:i * tile_shape + tile_shape - 1, j * tile_shape + 1:j * tile_shape + tile_shape - 1]

    sea_monster_str = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]

    sea_monster_arr = np.array([[1 if c == "#" else 0 for c in line]
                                for line in sea_monster_str], dtype=int)
    sea_monster_indices = np.argwhere(sea_monster_arr)

    index_matches, rotations = find_sea_monster(cropped_image, sea_monster_arr)
    rotation_matches = [(i_r, i)
                        for (i_r, i), v in index_matches.items() if len(v) > 0]
    signature_sea_monster = np.sum(sea_monster_arr)
    sum_image = np.sum(cropped_image)
    res = sum_image - \
        len(index_matches[rotation_matches[0]]) * signature_sea_monster
    print(res)

    if PLOT:
        sea_monster_highlighted = np.array(
            rotations[rotation_matches[0][0]][rotation_matches[0][1]])
        for i, j in index_matches[rotation_matches[0]]:
            sea_monster_highlighted[i:i + sea_monster_arr.shape[0],
                                    j:j + sea_monster_arr.shape[1]] *= sea_monster_arr * 10
        plt.figure(num="Cropped image with sea monsters")
        plt.imshow(sea_monster_highlighted)
        plt.show()
