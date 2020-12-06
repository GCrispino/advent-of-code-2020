with open('input/6.txt') as f:
    text = f.read()
    groups = text.split('\n\n')
    char_sets = [set(g.replace('\n', '')) for g in groups]

    res = sum([len(s) for s in char_sets])

    print(res)
