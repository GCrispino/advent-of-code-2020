ins_ops = {
    'nop': (lambda i, a, arg: (i + 1, a)),
    'acc': (lambda i, a, arg: (i + 1, a + arg)),
    'jmp': (lambda i, a, arg: (i + arg, a)),
}


def parse_instruction_str(ins_str):
    spl = ins_str.split(' ')
    return spl[0], int(spl[1])


def execute(instructions):
    acc = 0
    ins_id = 0
    executed = set([])

    while ins_id < len(instructions) and ins_id not in executed:
        executed.add(ins_id)
        ins, arg = instructions[ins_id]
        ins_id, acc = ins_ops[ins](ins_id, acc, arg)

    loop = ins_id < len(instructions)

    return acc, loop


with open('input/8.txt') as f:
    instructions = list(map(parse_instruction_str, f.readlines()))
    res = execute(instructions)
    print(res)
