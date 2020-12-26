import numpy as np

with open('input/13.txt') as f:
    lines = f.readlines()

    timestamp = int(lines[0])
    bus_ids_ = np.array([[i, int(e)]
                         for i, e in enumerate(lines[1].split(',')) if e != 'x'])

    i_bus_ids, bus_ids = bus_ids_.T

    prod_ts = bus_ids[0]
    t = 0
    for i in range(2, len(bus_ids) + 1):
        ts = bus_ids[:i]
        prod_ts = np.prod(ts[:i - 1])
        t += prod_ts
        while not np.all(((t + i_bus_ids[:i]) % bus_ids[:i]) == 0):
            t += prod_ts
    print(t)
