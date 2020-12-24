def parse_rule(rule):
    rule_id, body = rule.split(': ')
    if body[0] == '"':
        return rule_id, body.replace('"', '')
    spl_sub_rules = body.split(' | ')
    sub_rules = [x.split(' ') for x in spl_sub_rules]
    return rule_id, sub_rules


# This code is really ugly, but it works
def match_message_rule(rule, message, rules, indent=0, memo=None):
    memo = {} if memo == None else memo
    rule_body = rules[rule]
    if type(rule_body) == str:
        if len(message) == 0:
            return False, message
        match = message[0] == rule_body
        return match, message[1:]
    matched_subgroups = []
    for subrulegroup in rule_body:
        cur_message = message
        matched_subgroup = True
        for subrule in subrulegroup:
            if type(cur_message) == list:
                rests = []
                for m in cur_message:
                    if (subrule, m) in memo:
                        matched, message_rest = memo[(subrule, m)]
                    else:
                        matched, message_rest = match_message_rule(
                            subrule, m, rules, indent + 1, memo)
                        memo[(subrule, m)] = matched, message_rest
                    if matched:
                        rests.append(message_rest)
                matched = len(rests) > 0
                cur_message = rests
            else:
                if (subrule, cur_message) in memo:
                    matched, message_rest = memo[(subrule, cur_message)]
                else:
                    matched, message_rest = match_message_rule(
                        subrule, cur_message, rules, indent + 1, memo)
                    memo[(subrule, cur_message)] = matched, message_rest
                if not matched:
                    matched_subgroup = False
                    break
                cur_message = message_rest
        if matched_subgroup:
            if type(cur_message) == list:
                matched_subgroups.extend(cur_message)
            else:
                matched_subgroups.append(cur_message)
    if len(matched_subgroups) > 1:
        return True, matched_subgroups
    if len(matched_subgroups) == 1:
        return True, matched_subgroups[0]
    return False, message


with open('input/19-b.txt') as f:
    rules_str, messages_str = f.read().strip().split('\n\n')
    rule_lines = [r.strip() for r in rules_str.split('\n')]
    messages = [m.strip() for m in messages_str.split('\n')]
    rules = {}
    for l in rule_lines:
        rule_id, rule = parse_rule(l)
        rules[rule_id] = rule

    matched_messages = []
    for m in messages:
        matched, rests = match_message_rule('0', m, rules)
        if matched:
            if type(rests) == list and any([True for r in rests if r == '']):
                matched_messages.append(m)
            elif rests == '':
                matched_messages.append(m)

    print(len(matched_messages))
