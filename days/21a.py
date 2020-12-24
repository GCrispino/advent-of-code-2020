with open('input/21.txt') as f:
    lines = f.readlines()
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
    res = sum(safe_ingredients_counts)
    print(res)
