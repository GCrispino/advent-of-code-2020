def sign(n):
    return 1 if n > 0 else -1


def rotate(d, a, deg):
    factor = deg // 90 * (1 if a == 'R' else -1)
    n_cardinal = len(cardinal_actions_fns)
    cardinal_actions = list(cardinal_actions_fns.keys())
    new_d_ = cardinal_actions.index(d) + factor
    new_d = new_d_ if new_d_ < n_cardinal else new_d_ - n_cardinal

    return cardinal_actions[new_d]


def rotate_waypoint(state_w, a, deg):
    d_w, coord_w = state_w
    d_w_x, d_w_y = d_w
    new_d_w_x, new_d_w_y = d_w_x, d_w_y
    new_coord_w = coord_w
    for _ in range(deg // 90):
        new_d_w_x = rotate(new_d_w_x, a, 90)
        new_d_w_y = rotate(new_d_w_y, a, 90)
        if a == 'R':
            if new_d_w_x == 'E' or new_d_w_x == 'W':
                new_d_w_x, new_d_w_y = (new_d_w_y, new_d_w_x)
                new_coord_w = (new_coord_w[1], new_coord_w[0] * -1)
        if a == 'L':
            if new_d_w_x == 'E' or new_d_w_x == 'W':
                new_d_w_x, new_d_w_y = (new_d_w_y, new_d_w_x)
                new_coord_w = (new_coord_w[1] * -1, new_coord_w[0])
    return (new_d_w_x, new_d_w_y), new_coord_w


cardinal_coord_actions = {
    'N': lambda c, arg: (c[0] - arg, c[1]),
    'E': lambda c, arg: (c[0], c[1] + arg),
    'S': lambda c, arg: (c[0] + arg, c[1]),
    'W': lambda c, arg: (c[0], c[1] - arg)
}
cardinal_actions_fns = {
    'N': lambda s, arg: (s[0], (s[1][0], cardinal_coord_actions['N'](s[1][1], arg))),
    'E': lambda s, arg: (s[0], (s[1][0], cardinal_coord_actions['E'](s[1][1], arg))),
    'S': lambda s, arg: (s[0], (s[1][0], cardinal_coord_actions['S'](s[1][1], arg))),
    'W': lambda s, arg: (s[0], (s[1][0], cardinal_coord_actions['W'](s[1][1], arg))),
}


def rotate_fn(d):
    return lambda s, arg: (
        s[0],
        (
            rotate_waypoint(s[1], d, arg)
            #rotate_waypoint(s[1][0], d, arg)
            # s[1][1]
        )
    )


def move_forward(s, factor):
    s_x, s_y = s[0]
    w_x, w_y = s[1][1]
    move_units_x = w_x * factor
    move_units_y = w_y * factor

    new_state = ((s_x + move_units_x, s_y + move_units_y), s[1])
    return new_state


action_fns = {
    **cardinal_actions_fns,
    'L': rotate_fn('L'),
    'R': rotate_fn('R'),
    'F': move_forward
}


def apply_actions(state, actions):
    for a, arg in actions:
        state = action_fns[a](state, arg)
    return state


with open('input/12.txt') as f:
    actions = [(line[0], int(line[1:])) for line in f.readlines()]
    state = (
        (0, 0),
        (('N', 'E'), (-1, 10))
    )
    (final_x, final_y), _ = apply_actions(state, actions)
    res = abs(final_x) + abs(final_y)
    print("Final state:", final_x, final_y)
    print(res)
