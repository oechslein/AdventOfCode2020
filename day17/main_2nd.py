import itertools
from dataclasses import dataclass
from typing import Dict, Tuple

from Utils import count
from input import TEST_INPUT, PUZZLE_INPUT


def min_max(my_list):
    curr_min = curr_max = next(my_list)
    for elem in my_list:
        if elem > curr_max:
            curr_max = elem
        if elem < curr_min:
            curr_min = elem
    return curr_min, curr_max


@dataclass
class PocketDim(object):
    seed_dict: Dict[Tuple, bool]
    dimensions: int = 4

    def display(self, seed_dict: Dict[Tuple, bool]):
        dim_min_max = [(0, 0)] * self.dimensions
        for i in range(self.dimensions):
            dim_min_max[i] = min_max(cell[i] for cell in seed_dict)

        dim_names = 'xyzw'

        result = ['----------------------------------------------------------------------------------']
        for dims in itertools.product(*(range(dim_min, dim_max + 1) for dim_min, dim_max in dim_min_max[2:])):
            result.append(','.join(f'{name}: {dim_value}' for name, dim_value in zip(dim_names[2:], dims)))
            for y in range(dim_min_max[1][0], dim_min_max[1][1] + 1):
                x_result = ""
                for x in range(dim_min_max[0][0], dim_min_max[0][1] + 1):
                    x_result += '#' if seed_dict.get((x, y, *dims), False) else '.'
                result.append(x_result)
            result.append('')

        return '\n'.join(result)

    def neighbors(self, cell):
        distance = 1
        for neighbor_cell in itertools.product(*(range(dim_value - distance, dim_value + distance + 1) for dim_value in cell)):
            if cell != neighbor_cell:
                yield neighbor_cell, self.seed_dict.get(neighbor_cell, False)

    def get_active_inactive_neighbors_amount(self, cell):
        return sum(1 for neighbor_cell, neighbor_value in self.neighbors(cell) if neighbor_value)

    def update_cell(self, new_seed_dict: Dict[Tuple, bool], cell, value):
        active_neighbors = self.get_active_inactive_neighbors_amount(cell)
        if value:
            if active_neighbors not in (2, 3) and new_seed_dict.get(cell, False):
                del new_seed_dict[cell]
        else:
            if active_neighbors == 3:
                new_seed_dict[cell] = True

    def simulate(self, cycles: int, with_print=True, with_print_dim=False):
        for cycle_index in range(cycles):
            if with_print:
                print(f'After {cycle_index} cycles:')
                if with_print_dim:
                    print(self.display(self.seed_dict))
            new_seed_dict = self.seed_dict.copy()

            for cell, value in self.seed_dict.items():
                # check if current cells will change
                self.update_cell(new_seed_dict, cell, value)

                # check if we need to add neighbor cells that became active (non existing cells are inactive)
                assert count(self.neighbors(cell)) == (3**self.dimensions) - 1
                for neighbor_cell, neighbor_value in self.neighbors(cell):
                    self.update_cell(new_seed_dict, neighbor_cell, neighbor_value)

            self.seed_dict = new_seed_dict
        return self

    def count_active_states(self):
        return sum(1 for value in self.seed_dict.values() if value)


def parse_input(my_input_str: str) -> PocketDim:
    seed_dict = {}
    z = w = 0
    for y, line in enumerate(my_input_str.strip().split('\n')):
        for x, is_active in enumerate(line):
            if is_active == '#':  # All others are per default False
                seed_dict[(x, y, z, w)] = True
    return PocketDim(seed_dict)


assert parse_input(TEST_INPUT).simulate(6, with_print_dim=True).count_active_states() == 848
print(parse_input(PUZZLE_INPUT).simulate(6).count_active_states())
