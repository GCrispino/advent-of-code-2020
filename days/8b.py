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


def create_alternate_programs(program):
    programs = []
    for i, (ins, arg) in enumerate(program):
        if ins == 'nop':
            new_ins = ('jmp', arg)
        elif ins == 'jmp':
            new_ins = ('nop', arg)
        else:
            continue
        programs.append(program[:i] + [new_ins] + program[i + 1:])

    return programs


with open('input/8.txt') as f:
    program = list(map(parse_instruction_str, f.readlines()))
    programs = create_alternate_programs(program)
    for p in programs:
        acc, loop = execute(p)
        if not loop:
            print(acc)
