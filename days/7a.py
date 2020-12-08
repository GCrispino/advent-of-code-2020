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


def __search_containing_color(color, containing_color, rules, visited):
    #count = 1 if color == containing_color else 0
    if color == containing_color:
        visited[color] = 1
        return

    color_rules = rules[color]
    for color_rule in color_rules:
        if color_rule not in visited:
            __search_containing_color(color_rule,
                                      containing_color, rules, visited)
        if visited[color_rule]:
            visited[color] = 1
    if color not in visited:
        visited[color] = 0

    return


def search_containing_color(containing_color, rules):
    visited = {}
    for color in rules:
        if color not in visited:
            __search_containing_color(color,
                                      containing_color, rules, visited)
    return visited


color = 'shiny gold'
with open('input/7.txt') as f:
    lines = f.readlines()
    rules = parse_rules(lines)
    visited = search_containing_color(color, rules)
    res = sum([c for c in visited.values()]) - 1
    print(res)
