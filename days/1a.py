def get_result(entries):
    for x in entries:
        for y in entries:
            if x + y == 2020:
                return x * y
            if x + y > 2020:
                break
        if x + y > 2020:
            continue


with open('input/1.txt') as f:
    entries = sorted(map(int, f.readlines()))
    res = get_result(entries)
    print(res)
