import collections
import functools
import itertools
import operator
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, List

import numpy as np

from Utils import multiply, count
from input import PUZZLE_INPUT, TEST_INPUT

import sys

import re


# at least two sides need to fit to others
# only the corner tiles (always 4) have only two sides fitting
# inner tiles (x-2)*(x-2) have all sides fitting
# outer (not corner) ((x-2)*4) have 3 sides fitting
# amount of tiles is x * y
# image is always square => x * x

class Tile(object):
    def __init__(self, tile_number, tile_lines):
        self.tile_number = tile_number
        self.tile_lines = tile_lines

    def __repr__(self):
        return list(''.join(tile_line) for tile_line in self.tile_lines).__repr__()

    def rotate(self):
        return Tile(self.tile_number, np.rot90(self.tile_lines))

    def flip_x(self):
        return Tile(self.tile_number, np.fliplr(self.tile_lines))

    def flip_y(self):
        return Tile(self.tile_number, np.flipud(self.tile_lines))

    def get_border(self, border: int):
        if border == 0:
            return ''.join(self.tile_lines[0])
        elif border == 3:
            return ''.join(self.tile_lines[self.tile_lines.shape[0] - 1])
        elif border == 1:
            return ''.join(np.rot90(self.tile_lines)[0])
        elif border == 2:
            return ''.join(np.rot90(self.tile_lines)[self.tile_lines.shape[0] - 1])

    def get_all_borders(self):
        return {self.get_border(border) for border in range(4)}

    @functools.lru_cache(999)
    def get_all_possible_tiles(self, only_flipped=False):
        all_possible_tiles = {self}
        if not only_flipped:
            for _ in range(3):
                all_possible_tiles.add(self.rotate())
        for curr_tile in list(all_possible_tiles):
            all_possible_tiles.add(curr_tile.flip_x())
            all_possible_tiles.add(curr_tile.flip_y())
        return all_possible_tiles


def parse_input(my_input):
    def parse_tile(tile_str):
        tile_lines = tile_str.split('\n')
        tile_number = int(re.search(r'\d+', tile_lines[0]).group(0))
        tile_lines = tile_lines[1:]
        # np.array([list(tile_cell == '#' for tile_cell in tile) for tile in tile_lines])
        return Tile(tile_number, np.array([list(tile) for tile in tile_lines]))

    return [parse_tile(tile_str) for tile_str in my_input.strip().split('\n\n')]


def get_matching_sides(possible_tile_to_check, all_tiles):
    matching_sides = 0
    for tile in all_tiles:
        if tile.tile_number != possible_tile_to_check.tile_number:
            tile_all_borders = tile.get_all_borders()
            matching_sides += sum(1 for border in possible_tile_to_check.get_all_borders()
                                  if border in tile_all_borders)
    return matching_sides


def correct_tiles(tiles: List[Tile]):
    tiles_dict = {tile.tile_number: tile for tile in tiles}

    result = np.ndarray([len(tiles_dict), len(tiles_dict)], Tile)

    all_tiles = {possible_tiles for tile in tiles for possible_tiles in tile.get_all_possible_tiles(only_flipped=True)}

    corner_tiles = []
    for tile_to_check in tiles:
        for possible_tile_to_check in tile_to_check.get_all_possible_tiles():
            if get_matching_sides(possible_tile_to_check, all_tiles) == 2:
                corner_tiles.append(possible_tile_to_check)
                break

    return corner_tiles


# print(multiply(get_corner_tiles(correct_tiles(parse_input(PUZZLE_INPUT)))))


assert multiply(tile.tile_number for tile in correct_tiles(parse_input(TEST_INPUT))) == (1951 * 3079 * 2971 * 1171), \
    multiply(tile.tile_number for tile in correct_tiles(parse_input(TEST_INPUT)))

print(multiply(tile.tile_number for tile in correct_tiles(parse_input(PUZZLE_INPUT))))
