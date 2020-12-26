import math
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


def get_position_after_instructions(waypoint_position, ship_position, instructions: list):
    for next_instruction, next_instruction_argument in instructions:
        if next_instruction in 'NSWE':
            waypoint_position = get_position_after_direct_instruction(waypoint_position, next_instruction,
                                                                      next_instruction_argument)
        elif next_instruction == 'F':
            ship_position += waypoint_position * next_instruction_argument
        elif next_instruction == 'L':
            waypoint_position = rotate(waypoint_position, next_instruction_argument)
        elif next_instruction == 'R':
            waypoint_position = rotate(waypoint_position, -next_instruction_argument)
        else:
            assert False, (next_instruction, next_instruction_argument)
    return ship_position


def rotate(position, degree):
    degree_in_radians = degree / 180 * math.pi
    c, s = np.cos(degree_in_radians), np.sin(degree_in_radians)
    j = np.array([[c, s], [-s, c]])
    position = position
    position = np.dot(j, position).round().astype(int)
    return position


def manhatten_distance_after_instructions(instructions):
    start_waypoint_position = np.array((10, -1))
    start_ship_position = np.array((0, 0))
    end_ship_position = get_position_after_instructions(start_waypoint_position, start_ship_position.copy(),
                                                        instructions)
    return manhatten_distance(start_ship_position, end_ship_position)


assert manhatten_distance_after_instructions(parse_input(TEST_INPUT)) == (214 + 72), \
    manhatten_distance_after_instructions(parse_input(TEST_INPUT))

print(manhatten_distance_after_instructions(parse_input(PUZZLE_INPUT)))
