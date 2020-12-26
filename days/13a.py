import numpy as np

with open('input/13.txt') as f:
    lines = f.readlines()

    timestamp = int(lines[0])
    bus_ids = np.array([int(e) for e in lines[1].split(',') if e != 'x'])
    remainders = timestamp % bus_ids
    bus_timestamps = timestamp - remainders + bus_ids
    i_min_bus_timestamp = np.argmin(bus_timestamps)
    min_bus_timestamp = bus_timestamps[i_min_bus_timestamp]
    min_bus_id = bus_ids[i_min_bus_timestamp]
    res = (min_bus_timestamp - timestamp) * min_bus_id

    print(res)
