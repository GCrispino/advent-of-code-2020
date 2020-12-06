import numpy as np


def get_seat_info(bin_seat):
    bin_row = bin_seat[:7]
    bin_col = bin_seat[7:]

    starting_row = 0
    ending_row = 127
    for r in bin_row:
        mid = (ending_row - starting_row) // 2
        if r == 'F':
            ending_row -= mid + 1
        elif r == 'B':
            starting_row += mid + 1
    starting_col = 0
    ending_col = 7
    for c in bin_col:
        mid = (ending_col - starting_col) // 2
        if c == 'L':
            ending_col -= mid + 1
        elif c == 'R':
            starting_col += mid + 1
    seat_id = starting_row * 8 + starting_col
    return starting_row, starting_col, seat_id


with open('input/5.txt') as f:
    bin_seats = f.readlines()
    seats_info = np.array([get_seat_info(b) for b in bin_seats])
    ids = np.sort(seats_info.T[2])
    ids_ = np.concatenate([ids[1:], [0]])
    diff = ids_ - ids

    i_diff = np.argwhere((ids_ - ids) != 1).reshape(-1)[0]
    res = ids_[i_diff - 1] + 1
    print(res)
