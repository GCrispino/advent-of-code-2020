def create_node(x, nxt=None, prev=None, begin=False, end=False):
    return {'val': x, 'next': nxt, 'prev': prev, 'begin': begin, 'end': end}


def add(node, x):
    node['next'] = create_node(x, prev=node)
    return node


def search(node, x):
    point1 = node['next']
    point2 = node['prev']
    while point1['val'] != x and point2['val'] != x:
        point1 = point1['next']
        point2 = point2['prev']
    return point1 if point1['val'] == x else point2


def traverse(node, fn):
    ll = node
    while not ll['end']:
        fn(ll)
        ll = ll['next']
    fn(ll)


def from_list(l):
    llist = create_node(l[0], begin=True)
    prev = llist
    for i in range(1, len(l)):
        x = l[i]
        new_node = create_node(x, prev=prev)
        prev['next'] = new_node
        prev = new_node
    prev['end'] = True
    prev['next'] = llist
    llist['prev'] = prev
    return llist


def to_list(llist):
    l = []
    traverse(llist, lambda node: l.append(node['val']))

    return l


def move_sublist(source_node, dest_node, size=1):
    begin = source_node['begin']
    end = dest_node['end']
    before_source_node = source_node['prev']
    last_node_sublist = source_node
    for _ in range(size - 1):
        last_node_sublist = last_node_sublist['next']
    next_to_last_node_sublist = last_node_sublist['next']
    #next_to_next_to_last_node_sublist = next_to_last_node_sublist['next']
    next_to_dest_node = dest_node['next']

    dest_node['next'] = source_node
    source_node['prev'] = dest_node
    if begin:
        dest_node['begin'] = True
        source_node['begin'] = False

    before_source_node['next'] = next_to_last_node_sublist
    next_to_last_node_sublist['prev'] = before_source_node

    last_node_sublist['next'] = next_to_dest_node
    next_to_dest_node['prev'] = last_node_sublist

    if end:
        last_node_sublist['end'] = True
        dest_node['end'] = False


if __name__ == '__main__':
    l = [3, 2, 8, 9, 1, 5, 4, 6, 7]
    ll = from_list(l)
    llist = from_list(l)
    while not llist['end']:
        print(llist['val'], end=" ")
        llist = llist['next']
    print(llist['val'])

    print(to_list(ll))
    source_node = ll['next']
    dest_node = source_node['next']['next']['next']
    #dest_node = ll['prev']['prev']
    move_sublist(source_node, dest_node, size=3)
    print(to_list(ll))
