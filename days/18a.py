import operator as op
import re

operator_fn = {
    '+': op.add,
    '*': op.mul
}


def get_index_closing_par(expr, offset=0):
    stack = []
    for j, t in enumerate(expr[offset:]):
        if t == '(':
            stack.append('(')
        elif t == ')':
            stack.pop()
            if len(stack) == 0:
                break
    return offset + j


def eval_paren_expr(expr, offset=0):
    i_closing_par = get_index_closing_par(expr, offset)
    return eval_expr(expr[offset + 1:i_closing_par]), i_closing_par


def eval_expr(expr):
    if expr[0] == '(':
        eval_paren, i_closing_par = eval_paren_expr(expr)

        return eval_expr(str(eval_paren) + expr[i_closing_par + 1:])

    operator_match = re.search(r'\+|\*', expr)
    if not operator_match:
        return int(expr)

    i_operator = operator_match.span()[0]
    operator = expr[i_operator]
    arg1 = int(expr[:i_operator])

    nxt_token = expr[i_operator + 1]
    if nxt_token == '(':
        eval_paren, i_closing_par = eval_paren_expr(expr, i_operator + 1)
        res = operator_fn[operator](arg1, eval_paren)

        return eval_expr(str(res) + expr[i_closing_par + 1:])
    else:
        operator_match = re.search(r'\+|\*', expr[i_operator + 1:])
        if not operator_match:
            arg2 = int(expr[i_operator + 1:])
            res = operator_fn[operator](arg1, arg2)
            return res

        i_operator_ = i_operator + 1 + operator_match.span()[0]
        arg2 = int(expr[i_operator + 1:i_operator_])
        res = operator_fn[operator](arg1, arg2)
        return eval_expr(str(res) + expr[i_operator_:])


with open('input/18.txt') as f:
    exprs = [expr.replace(' ', '').strip() for expr in f.readlines()]
    res_ = list(map(eval_expr, exprs))
    res = sum(res_)
    print(res)
