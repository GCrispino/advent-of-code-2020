from time import time

import utils.llist as llist


def get_i(i_x, offset, length):
    i_x_ = i_x + offset
    return i_x_ if i_x_ < length else i_x_ - length


def get_res(ns, init=1):
    i_1 = ns.index(init)
    return ns[i_1 + 1] * ns[i_1 + 2]


def create_node_list(ns, length):
    l = [None] * length

    def fn(node):
        l[node['val'] - 1] = node
    llist.traverse(ns, fn)

    return l


#input_data = '389125467'
input_data = '942387615'

print("Creating lists...")
ns_ = list(map(int, list(input_data)))
ns_initial = ns_ + list(range(max(ns_) + 1, 1000001))
nn = len(ns_initial)
ns = llist.from_list(ns_initial)
node_list = create_node_list(ns, nn)
print(" ...done")

max_n = max(ns_initial)
min_n = min(ns_initial)
i_x = 0
first_node = ns
current_node = ns

for i in range(10000000):
    if i % 500000 == 0:
        print('Iteration', i + 1)

    # Find first pick by getting next node from current cup
    x = current_node['val']
    first_pick_node = current_node['next']
    second_pick_node = first_pick_node['next']
    third_pick_node = second_pick_node['next']
    picks = (first_pick_node['val'],
             second_pick_node['val'], third_pick_node['val'])

    # Find destination value and corresponding node
    begin = time()
    x_dest = x - 1 if x > min_n else max_n
    while x_dest in picks:
        x_dest = x_dest - 1 if x_dest > min_n else max_n

    dest_node = node_list[x_dest - 1]

    # Move picks in linked list
    llist.move_sublist(first_pick_node, dest_node, size=3)
    if dest_node['begin']:
        first_node = dest_node

    i_x = i_x + 1 if i_x < nn - 1 else 0
    current_node = current_node['next']

final = llist.to_list(first_node)
node_1 = llist.search(first_node, 1)
res = node_1['next']['val'] * node_1['next']['next']['val']
print(res)
