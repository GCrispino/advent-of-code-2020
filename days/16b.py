import functools
from math import prod


def parse_rule(rule_txt):
    rules = rule_txt.split(' or ')
    parsed_rules = []
    for r in rules:
        start, end = r.split('-')
        parsed_rules.append((int(start), int(end)))
    return parsed_rules


def parse_rules(rules_txt):
    lines = rules_txt.split('\n')
    rules = {}
    for x in lines:
        spl = x.split(': ')
        name = spl[0]
        rules[name] = parse_rule(spl[1])
    return rules


def parse_ticket(ticket):
    return list(map(int, ticket.split(',')))


def validate_field(rules, value):
    for rs in rules.values():
        rule1, rule2 = rs
        rule1_valid = rule1[0] <= value <= rule1[1]
        rule2_valid = rule2[0] <= value <= rule2[1]
        if rule1_valid or rule2_valid:
            return True

    return False


def validate_ticket(rules, ticket):
    return all([validate_field(rules, value) for value in ticket])


def get_invalid_fields(rules, value):
    cant = set([])
    for name, rs in rules.items():
        rule1, rule2 = rs
        rule1_valid = rule1[0] <= value <= rule1[1]
        rule2_valid = rule2[0] <= value <= rule2[1]
        if (not rule1_valid) and (not rule2_valid):
            cant.add(name)

    return cant


def get_fields(rules, valid_tickets):
    n_rules = len(rules)
    n_tickets = len(valid_tickets)

    invalid_fields = []
    used_fields = set([])
    rule_set = set(rules)
    fields = [None] * n_rules
    while not all(fields):
        for j in range(n_rules):
            cant = set(used_fields)
            for i in range(n_tickets):
                value = valid_tickets[i][j]
                cant.update(get_invalid_fields(rules, value))
            possible_fields = rule_set - cant
            if len(possible_fields) == 1:
                field = possible_fields.pop()
                fields[j] = field
                used_fields.add(field)
            invalid_fields.append(cant)

    return fields


with open('input/16.txt') as f:
    spl = f.read().split('\n\n')
    rules = parse_rules(spl[0])
    my_ticket = parse_ticket(spl[1].split('\n')[1])
    nearby_tickets = list(map(parse_ticket, spl[2].strip().split('\n')[1:]))

    valid_tickets = list(filter(functools.partial(
        validate_ticket, rules), nearby_tickets))

    fields = get_fields(rules, valid_tickets)
    i_departure_fields = [i for i, x in enumerate(
        fields) if x[:9] == "departure"]
    departure_values = [my_ticket[i] for i in i_departure_fields]
    res = prod(departure_values)
    print(res)
