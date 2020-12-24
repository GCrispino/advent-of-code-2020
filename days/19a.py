def parse_rule(rule):
    rule_id, body = rule.split(': ')
    if body[0] == '"':
        return rule_id, body.replace('"', '')
    spl_sub_rules = body.split(' | ')
    sub_rules = [x.split(' ') for x in spl_sub_rules]
    return rule_id, sub_rules


def match_message_rule(rule, message, rules):
    rule_body = rules[rule]
    if type(rule_body) == str:
        return message[0] == rule_body, message[1:]
    for subrulegroup in rule_body:
        cur_message = message
        matched_subgroup = True
        for subrule in subrulegroup:
            matched, message_rest = match_message_rule(
                subrule, cur_message, rules)
            if not matched:
                matched_subgroup = False
                break
            cur_message = message_rest
        if matched_subgroup:
            return True, cur_message
    return False, ""


with open('input/19.txt') as f:
    rules_str, messages_str = f.read().strip().split('\n\n')
    rule_lines = [r.strip() for r in rules_str.split('\n')]
    messages = [m.strip() for m in messages_str.split('\n')]
    rules = {}
    for l in rule_lines:
        rule_id, rule = parse_rule(l)
        rules[rule_id] = rule

    matched_messages = []
    for m in messages:
        matched, rest = match_message_rule('0', m, rules)
        if matched and len(rest) == 0:
            matched_messages.append(m)
    print(len(matched_messages))
