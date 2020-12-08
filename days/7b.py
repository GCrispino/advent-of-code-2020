import re
from pprint import pprint


def parse_color_rules(str_color_rules):
    spl = str_color_rules[8:].split(', ')
    color_rules = {}
    qty_re = re.compile(r'\d+')
    for r in spl:
        match_qty = qty_re.match(r)
        if not match_qty:
            continue
        match_span = match_qty.span()
        qty = int(r[match_span[0]:match_span[1]])
        color_rules[r[match_span[1] + 1:].split(' bag')[0]] = qty
    return color_rules


def parse_rule(line):
    spl = line.split(' bags ')
    color_rules = parse_color_rules(spl[1])
    return (spl[0], color_rules)


def parse_rules(input_lines):
    rules = {}
    for line in input_lines:
        k, v = parse_rule(line.strip())
        rules[k] = v
    return rules


def get_n_bags(color, rules, memory=None):
    memory = {} if memory == None else memory
    count = 0

    for c, n in rules[color].items():
        if c not in memory:
            memory[c] = get_n_bags(c, rules, memory)
        count += n + n * memory[c]

    memory[color] = count
    return count


color = 'shiny gold'
with open('input/7.txt') as f:
    lines = f.readlines()
    rules = parse_rules(lines)
    res = get_n_bags(color, rules)
    print(res)
