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
    invalids = []
    for value in ticket:
        res = validate_field(rules, value)
        if not res:
            invalids.append(value)
    return invalids


with open('input/16.txt') as f:
    spl = f.read().split('\n\n')
    rules = parse_rules(spl[0])
    my_ticket = parse_ticket(spl[1].split('\n')[1])
    nearby_tickets = list(map(parse_ticket, spl[2].strip().split('\n')[1:]))

    res = sum([sum(validate_ticket(rules, tkt)) for tkt in nearby_tickets])
    print(res)
