def get_result(entries):
    for x in entries:
        for y in entries:
            for z in entries:
                if x + y + z == 2020:
                    return x * y * z
                if x + y + z > 2020:
                    break


with open('input/1.txt') as f:
    entries = sorted(map(int, f.readlines()))
    res = get_result(entries)
    print(res)
