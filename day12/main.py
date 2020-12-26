import re

import numpy as np

from input import TEST_INPUT, PUZZLE_INPUT


def parse_input(my_input):
    return list((result := re.fullmatch(r'([A-Z])(\d+)', instruction))
                and (result[1], int(result[2]))
                for instruction in my_input.strip().split('\n'))


def manhatten_distance(start, end):
    return abs((end - start)).sum()


def get_position_after_direct_instruction(position, instruction, instruction_argument):
    if instruction == 'N':
        position += np.array((0, -instruction_argument))
    elif instruction == 'S':
        position += np.array((0, instruction_argument))
    elif instruction == 'W':
        position += np.array((-instruction_argument, 0))
    elif instruction == 'E':
        position += np.array((instruction_argument, 0))
    else:
        assert False, instruction
    return position


def get_position_after_instructions(position, direction, instructions: list):
    directions = 'NESW'
    if not instructions:
        return position
    next_instruction, next_instruction_argument = instructions[0]
    if next_instruction in 'NSWE':
        position = get_position_after_direct_instruction(position, next_instruction, next_instruction_argument)
    elif next_instruction == 'F':
        position = get_position_after_direct_instruction(position, direction, next_instruction_argument)
    elif next_instruction == 'L':
        direction = directions[(directions.find(direction) - next_instruction_argument // 90) % len(directions)]
    elif next_instruction == 'R':
        direction = directions[(directions.find(direction) + next_instruction_argument // 90) % len(directions)]
    else:
        assert False, (next_instruction, next_instruction_argument)
    return get_position_after_instructions(position, direction, instructions[1:])


def manhatten_distance_after_instructions(instructions):
    start_position = np.array((0, 0))
    start_direction = 'E'
    end_position = get_position_after_instructions(start_position.copy(), start_direction, instructions)
    return manhatten_distance(start_position, end_position)


assert manhatten_distance(np.array((0, 0)), np.array((17, 8))) == 25
assert manhatten_distance_after_instructions(parse_input(TEST_INPUT)) == 25, \
    manhatten_distance_after_instructions(parse_input(TEST_INPUT))

print(manhatten_distance_after_instructions(parse_input(PUZZLE_INPUT)))
