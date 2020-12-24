from itertools import chain
from random import shuffle
from copy import deepcopy

with open('input/21.txt') as f:
    lines = f.readlines()
    for i in range(100):
        shuffle(lines)
    rules = []
    all_ingredients = set([])
    for l in lines:
        spl = l.strip().split(' (')
        ingredients = spl[0].split(' ')
        all_ingredients.update(set(ingredients))
        allergens = spl[1][9:-1].split(', ')
        rules.append((ingredients, allergens))

    allergens_candidates = {}
    ingredient_occurences_count = {i: 0 for i in all_ingredients}
    for ingredients, allergens in rules:
        ingredient_set = set(ingredients)
        for i in ingredient_set:
            ingredient_occurences_count[i] += 1
        for a in allergens:
            if a not in allergens_candidates:
                allergens_candidates[a] = ingredient_set
            else:
                allergens_candidates[a] = allergens_candidates[a].intersection(
                    ingredient_set)

    result_set = set.union(*allergens_candidates.values())
    safe_ingredients = all_ingredients - result_set
    safe_ingredients_counts = [
        ingredient_occurences_count[i] for i in safe_ingredients]

    # cleanup
    allergens_final = deepcopy(allergens_candidates)
    candidates_once = set([next(iter(c))
                           for c in allergens_final.values() if len(c) == 1])
    candidates_multiple = {a: c
                           for a, c in allergens_final.items() if len(c) > 1}
    stack = list(candidates_once)
    set_multiple = set(candidates_multiple)
    while stack:
        allergen = stack.pop()
        for ingr in set_multiple:
            if ingr not in candidates_multiple:
                continue
            if allergen in candidates_multiple[ingr]:
                candidates_multiple[ingr] -= set([allergen])
                if len(candidates_multiple[ingr]) == 1:
                    stack.append(next(iter(candidates_multiple[ingr])))
                    candidates_multiple.pop(ingr)

    sorted_allergens_final = sorted(
        allergens_final.items())
    res = ",".join([next(iter(a[1])) for a in sorted_allergens_final])
    print(res)
