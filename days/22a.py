def play_game(deck_1, deck_2):
    d1, d2 = list(deck_1), list(deck_2)
    while len(d1) > 0 and len(d2) > 0:
        c1, c2 = d1.pop(), d2.pop()
        if c1 > c2:
            winning_d = d1
            winning_c, losing_c = c1, c2
        elif c1 < c2:
            winning_d = d2
            winning_c, losing_c = c2, c1
        else:
            exit("Error!")
        winning_d.insert(0, winning_c)
        winning_d.insert(0, losing_c)
    if len(d1) > 0:
        return d1
    else:
        return d2


with open('input/22.txt') as f:
    deck_strs = f.read().strip().split('\n\n')

    decks = [[int(c) for c in ds.split('\n')[1:]][::-1]
             for ds in deck_strs]
    winning_deck = play_game(*decks)
    score = sum([c * (i + 1) for i, c in enumerate(winning_deck)])
    print(score)
