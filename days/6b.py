def get_questions_answered_by_all(group):
    entries = {}
    lines = group.split('\n')
    n_lines = len(lines)
    for line in lines:
        for c in line:
            if c not in entries:
                entries[c] = 1
            else:
                entries[c] += 1
    all_answered = [k for k, v in entries.items() if v == n_lines]
    return all_answered


with open('input/6.txt') as f:
    text = f.read()
    groups = text.split('\n\n')
    res = sum([len(get_questions_answered_by_all(g.strip())) for g in groups])

    print(res)
