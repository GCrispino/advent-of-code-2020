def rotate(d, a, deg):
    factor = deg // 90 * (1 if a == 'R' else -1)
    n_cardinal = len(cardinal_actions_fns)
    cardinal_actions = list(cardinal_actions_fns.keys())
    new_d_ = cardinal_actions.index(d) + factor
    new_d = new_d_ if new_d_ < n_cardinal else new_d_ - n_cardinal

    return cardinal_actions[new_d]


cardinal_actions_fns = {
    'N': lambda s, arg: (s[0], (s[1][0] - arg, s[1][1])),
    'E': lambda s, arg: (s[0], (s[1][0], s[1][1] + arg)),
    'S': lambda s, arg: (s[0], (s[1][0] + arg, s[1][1])),
    'W': lambda s, arg: (s[0], (s[1][0], s[1][1] - arg))
}

action_fns = {
    **cardinal_actions_fns,
    'L': lambda s, arg: (rotate(s[0], 'L', arg), (s[1][0], s[1][1])), 'R': lambda s, arg: (rotate(s[0], 'R', arg), (s[1][0], s[1][1])), 'F': lambda s, arg: action_fns[s[0]]((s[0], (s[1][0], s[1][1])), arg)
}


def apply_actions(state, actions):
    for a, arg in actions:
        state = action_fns[a](state, arg)
    return state


with open('input/12.txt') as f:
    actions = [(line[0], int(line[1:])) for line in f.readlines()]
    state = ('E', (0, 0))
    _, (final_x, final_y) = apply_actions(state, actions)
    res = abs(final_x) + abs(final_y)
    print("Final state:", final_x, final_y)
    print(res)
