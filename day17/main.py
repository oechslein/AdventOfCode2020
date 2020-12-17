import collections
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

from input import TEST_INPUT, PUZZLE_INPUT


def min_max(my_list):
    curr_min = curr_max = next(my_list)
    for elem in my_list:
        curr_min = min(curr_min, elem)
        curr_max = max(curr_max, elem)
    return curr_min, curr_max

@dataclass
class PocketDim(object):
    seed_dict: Dict[Tuple[int, int, int], bool]

    @staticmethod
    def set_active(cell):
        cell[3] = 1

    @staticmethod
    def set_inactive(cell):
        cell[3] = 0

    @staticmethod
    def x(cell):
        return cell[0]

    @staticmethod
    def y(cell):
        return cell[1]

    @staticmethod
    def z(cell):
        return cell[2]

    @staticmethod
    def display(seed_dict: Dict[Tuple[int, int, int], bool]):
        min_x, max_x = min_max(PocketDim.x(cell) for cell in seed_dict)
        min_y, max_y = min_max(PocketDim.y(cell) for cell in seed_dict)
        min_z, max_z = min_max(PocketDim.z(cell) for cell in seed_dict)

        result = ['----------------------------------------------------------------------------------']
        for z in range(min_z, max_z+1):
            result.append(f'z={z}')
            for y in range(min_y, max_y + 1):
                x_result = ""
                for x in range(min_x, max_x+1):
                    x_result += '#' if seed_dict.get(PocketDim.create_cell(x, y, z), False) else '.'
                result.append(x_result)
            result.append('')

        return '\n'.join(result)

    @staticmethod
    def create_cell(x, y, z):
        return x, y, z

    def neighbors(self, cell, direct_only=True):
        distance = 1 if direct_only else 2
        for diff_x in range(-distance, distance+1):
            for diff_y in range(-distance, distance + 1):
                for diff_z in range(-distance, distance + 1):
                    neighbor_cell = PocketDim.create_cell(PocketDim.x(cell) + diff_x, PocketDim.y(cell) + diff_y, PocketDim.z(cell) + diff_z)
                    if cell != neighbor_cell:
                        yield neighbor_cell, self.seed_dict.get(neighbor_cell, False)

    def get_active_inactive_neighbors_amount(self, cell):
        return sum(1 for neighbor_cell, neighbor_value in self.neighbors(cell) if neighbor_value)

    def update_cell(self, new_seed_dict: Dict[Tuple[int, int, int], bool], cell, value):
        active_neighbors = self.get_active_inactive_neighbors_amount(cell)
        if value:
            if active_neighbors not in (2, 3) and new_seed_dict.get(cell, False):
                del new_seed_dict[cell]
        else:
            if active_neighbors == 3:
                new_seed_dict[cell] = True

    def simulate(self, cycles: int, with_print=False):
        for _ in range(cycles):
            if with_print:
                print(PocketDim.display(self.seed_dict))
            new_seed_dict = self.seed_dict.copy()

            for cell, value in self.seed_dict.items():
                # check if current cells will change
                self.update_cell(new_seed_dict, cell, value)

                # check if we need to add neighbor cells that became active (non existing cells are inactive)
                for neighbor_cell, neighbor_value in self.neighbors(cell, True):
                    self.update_cell(new_seed_dict, neighbor_cell, neighbor_value)

            self.seed_dict = new_seed_dict
        return self

    def count_active_states(self):
        return sum(1 for value in self.seed_dict.values() if value)


def parse_input(my_input_str: str) -> PocketDim:
    seed_dict = {}  # collections.defaultdict(lambda: False)
    z = 0
    for y, line in enumerate(my_input_str.strip().split('\n')):
        for x, is_active in enumerate(line):
            if is_active == '#':  # All others are per default False
                seed_dict[(x, y, z)] = True
    return PocketDim(seed_dict)


assert parse_input(TEST_INPUT).simulate(6, with_print=False).count_active_states() == 112
print(parse_input(PUZZLE_INPUT).simulate(6).count_active_states())
