import re
from collections import namedtuple

from day8_input import TEST_INPUT, PUZZLE_INPUT

instruction_type = namedtuple("instruction_type", ["opp", "arg"])


def parse_input(my_input):
    def parse_line(line):
        result = re.fullmatch(r'([^ ]+) ([+\-\d]+)', line)
        return instruction_type(result[1], int(result[2]))

    return list(map(parse_line, my_input.strip().split('\n')))


def interpret_program(program):
    visited_program_counters = set()
    program_counter = 0
    accumulator = 0
    while program_counter not in visited_program_counters and program_counter < len(program):
        visited_program_counters.add(program_counter)
        curr_opp = program[program_counter].opp
        if curr_opp == "nop":
            pass
        elif curr_opp == "acc":
            accumulator += program[program_counter].arg
        elif curr_opp == "jmp":
            program_counter += program[program_counter].arg - 1
        else:
            assert False, curr_opp
        program_counter += 1
    return program_counter >= len(program), accumulator


assert interpret_program(parse_input(TEST_INPUT)) == (False, 5), interpret_program(parse_input(TEST_INPUT))

print(interpret_program(parse_input(PUZZLE_INPUT)))


## 2nd

def gen_changed_programs(original_program):
    for index, instruction in enumerate(original_program):
        if instruction.opp == 'nop':
            yield original_program[:index] + [instruction_type('jmp', instruction.arg)] + original_program[index + 1:]
        elif instruction.opp == 'jmp':
            yield original_program[:index] + [instruction_type('nop', instruction.arg)] + original_program[index + 1:]
        else:
            pass


def correct_program(program):
    for modified_program in gen_changed_programs(program):
        result, accumulator = interpret_program(modified_program)
        if result:
            return accumulator


assert correct_program(parse_input(TEST_INPUT)) == 8, correct_program(parse_input(TEST_INPUT))

print(correct_program(parse_input(PUZZLE_INPUT)))
