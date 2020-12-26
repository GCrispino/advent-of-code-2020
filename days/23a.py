def get_i(i_x, offset, length):
    i_x_ = i_x + offset
    return i_x_ if i_x_ < length else i_x_ - length


def get_order(ns, init=1):
    nn = len(ns)
    i_init = ns.index(init) + 1
    i_end = i_init + nn
    order = []
    for i in range(i_init, i_end - 1):
        final_i = get_i(i, 0, nn)
        order.append(ns[final_i])
    return ''.join(map(str, order))


#input_data = '389125467'
input_data = '942387615'

ns = list(map(int, list(input_data)))

max_n = max(ns)
min_n = min(ns)
nn = len(ns)
i_x = 0
for i in range(100):
    x = ns[i_x]
    i_picks = [get_i(i_x, j, nn) for j in range(1, 4)]
    picks = [ns[j] for j in i_picks]

    x_dest = x - 1 if x > min_n else max_n
    while x_dest in picks:
        x_dest = x_dest - 1 if x_dest > min_n else max_n
    i_x_dest = ns.index(x_dest)

    start = i_picks[0]
    end = (i_x_dest if start < i_x_dest < nn else i_x_dest + nn) - 2
    for j in range(start, end):
        j_0 = get_i(j, 0, nn)
        j_1 = get_i(j, 1, nn)
        j_2 = get_i(j, 2, nn)
        j_3 = get_i(j, 3, nn)

        ns[j_2], ns[j_3] = ns[j_3], ns[j_2]
        ns[j_1], ns[j_2] = ns[j_2], ns[j_1]
        ns[j_0], ns[j_1] = ns[j_1], ns[j_0]

    i_x = i_x + 1 if i_x < nn - 1 else 0

res = get_order(ns)
print(res)
