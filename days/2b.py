with open('input/2.txt') as f:
    entries = [((spl:= line.split(':'))[0].split(' '), spl[1][1:-1])
               for line in f.readlines()]
    res = sum([1 for (rng, char), password in entries if
               (password[int((x:= rng.split('-'))[0]) - 1] == char) ^ (password[int(x[1]) - 1] == char)])
    print(res)
