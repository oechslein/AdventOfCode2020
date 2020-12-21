import collections
import functools
import heapq
import itertools
import math
import operator
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, List

import numpy as np

import Utils
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
    def __init__(self, tile_number: int, tile_lines: np.ndarray):
        self.tile_number = tile_number
        self.tile_lines = tile_lines
        self.tile_lines.flags.writeable = False
        self.__hash = hash((tile_number, self.as_tuple()))

    def __hash__(self):
        return self.__hash

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return (self.tile_number == other.tile_number) and (self.tile_lines == other.tile_lines).all()

    @classmethod
    def parse_tile(cls, tile_str):
        tile_lines = tile_str.split('\n')
        tile_number = int(re.search(r'\d+', tile_lines[0]).group(0))
        tile_lines = tile_lines[1:]
        return Tile(tile_number, np.array([list(tile) for tile in tile_lines]))

    def __repr__(self):
        return str(self.tile_number) + "/" + self.as_tuple().__repr__()

    def as_tuple(self):
        return tuple(''.join(tile_line) for tile_line in self.tile_lines)

    @property
    def shape(self):
        return self.tile_lines.shape

    @property
    def width(self):
        return self.shape[0]

    @property
    def height(self):
        return self.shape[1]

    def rotate(self, amount):
        return Tile(self.tile_number, np.rot90(self.tile_lines, k=-amount, axes=(1, 0)))

    def flip_x(self):
        return Tile(self.tile_number, np.fliplr(self.tile_lines))

    def flip_y(self):
        return Tile(self.tile_number, np.flipud(self.tile_lines))

    def _tile_line_to_number(self, tile_line):
        return int(''.join(tile_line).replace('.', '0').replace('#', '1'), base=2)

    @functools.lru_cache(999)
    def get_border(self, border: int):
        if border == 0:
            return self._tile_line_to_number(self.tile_lines[0])
        elif border == 1:
            return self._tile_line_to_number(np.rot90(self.tile_lines, k=-1, axes=(1, 0))[0])
        elif border == 2:
            return self._tile_line_to_number(self.tile_lines[self.width - 1])
        elif border == 3:
            return self._tile_line_to_number(np.rot90(self.tile_lines, k=-1, axes=(1, 0))[self.height - 1])

    @functools.lru_cache(999)
    def get_all_borders(self):
        return frozenset(self.get_border(border) for border in range(4))

    @functools.lru_cache(999)
    def get_all_possible_tiles(self, only_flipped=False):
        all_possible_tiles = {self}
        if not only_flipped:
            for i in range(1, 4):
                all_possible_tiles.add(self.rotate(i))
        for curr_tile in list(all_possible_tiles):
            all_possible_tiles.add(curr_tile.flip_x())
            all_possible_tiles.add(curr_tile.flip_y())
        return all_possible_tiles

    def remove_borders(self):
        new_tile_lines = np.ndarray((self.width - 2, self.height - 2), self.tile_lines.dtype)
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                new_tile_lines[x - 1, y - 1] = self.tile_lines[x, y]
        return Tile(self.tile_number, new_tile_lines)


class TilesSolver(object):
    def __init__(self, tiles):
        self.tiles = tiles
        self.shape = (math.isqrt(len(self.tiles)),) * 2
        self.tile_possibilities = self.create_tile_possibilities_array()

    def create_tile_possibilities_array(self):
        possibilities = np.ndarray((self.width, self.height), set)
        corner_tiles = self.get_corner_tiles()
        first_corner_tile_number = list(self.get_corner_tile_numbers())[0] \
            if 1951 not in self.get_corner_tile_numbers() \
            else 1951

        for x in range(self.width):
            for y in range(self.height):
                if (x, y) == (0, 0):
                    possibilities[x, y] = {corner_tile for corner_tile in corner_tiles
                                           if corner_tile.tile_number == first_corner_tile_number}
                elif (x, y) in ((self.width - 1, 0), (0, self.height - 1), (self.width - 1, self.height - 1)):
                    possibilities[x, y] = {corner_tile for corner_tile in corner_tiles
                                           if corner_tile.tile_number != first_corner_tile_number}
                else:
                    possibilities[x, y] = {tile for tile in self.get_all_tiles()
                                           if tile.tile_number not in self.get_corner_tile_numbers()}
        return possibilities

    @property
    def width(self):
        return self.shape[0]

    @property
    def height(self):
        return self.shape[1]

    @functools.lru_cache(999)
    @Utils.listify
    def get_neighbors(self, x, y):
        if y > 0:
            yield x, y - 1, 0
        if x < self.width - 1:
            yield x + 1, y, 1
        if y < self.height - 1:
            yield x, y + 1, 2
        if x > 0:
            yield x - 1, y, 3

    def get_tile_possibilities(self, x, y):
        return self.tile_possibilities[x, y]

    def get_tile_possibilities_lens(self):
        lens_array = np.ndarray(self.shape, int)
        for x in range(self.width):
            for y in range(self.height):
                lens_array[x, y] = len(self.tile_possibilities[x, y])
        return lens_array

    def get_tile_possibilities_count(self):
        tile_possibilities_count = 1
        for x in range(self.width):
            for y in range(self.height):
                tile_possibilities_count *= len(self.tile_possibilities[x, y])
        return tile_possibilities_count

    @functools.lru_cache(999)
    def border_fits(self, tile, neighbor_tile, direction):
        neighbor_direction = (direction + 2) % 4
        return tile.get_border(direction) == neighbor_tile.get_border(neighbor_direction)

    def remove_used_tile_number(self, x, y):
        used_tile_number = list(self.tile_possibilities[x, y])[0].tile_number
        for y2 in range(self.height):
            for x2 in range(self.width):
                if (x, y) != (x2, y2):
                    self.tile_possibilities[x2, y2] = {tile for tile in self.tile_possibilities[x2, y2]
                                                       if tile.tile_number != used_tile_number}

    def remove_wrong_possibilities(self):
        removed_possibilities = True
        while removed_possibilities:
            removed_possibilities = False
            prev_x = prev_y = None
            for y in range(self.height):
                for x in reversed(range(self.width)) if y % 2 else range(self.width):
                    for tile in list(self.tile_possibilities[x, y]):
                        prev_directions = [direction for n_x, n_y, direction in self.get_neighbors(x, y)
                                           if (n_x, n_y) == (prev_x, prev_y)]
                        fits = True
                        if prev_directions:
                            assert len(prev_directions) == 1
                            prev_direction = prev_directions[0]
                            fits = any(self.border_fits(tile, neighbor_tile, prev_direction)
                                       for neighbor_tile in self.get_tile_possibilities(prev_x, prev_y))

                        if fits and not removed_possibilities:
                            fits = all(any(self.border_fits(tile, neighbor_tile, direction)
                                           for neighbor_tile in self.get_tile_possibilities(neighbor_x, neighbor_y))
                                       for neighbor_x, neighbor_y, direction in self.get_neighbors(x, y))
                        if not fits:
                            self.tile_possibilities[x, y].remove(tile)
                            removed_possibilities = True
                            assert len(self.tile_possibilities[x, y]) >= 1
                    prev_x, prev_y = x, y
                    if len({tile.tile_number for tile in self.tile_possibilities[x, y]}) == 1:
                        if len(self.tile_possibilities[x, y]) == 2 and (x, y) == (0, 0):
                            self.tile_possibilities[x, y] = {list(self.tile_possibilities[x, y])[1]}
                        self.remove_used_tile_number(x, y)
        if all(len(self.tile_possibilities[x, y]) == 2 for x in range(self.width) for y in range(self.height)):
            self.tile_possibilities[0, 0] = {list(self.tile_possibilities[0, 0])[1]}
            self.remove_wrong_possibilities()
        assert all(len(self.tile_possibilities[x, y]) == 1 for x in range(self.width) for y in range(self.height))

    def get_tile_array(self):
        tile_array = np.ndarray((self.width, self.height), Tile)
        for x in range(self.width):
            for y in range(self.height):
                tile_array[x, y] = list(self.get_tile_possibilities(x, y))[0]
        return tile_array

    def remove_borders(self, tile_array):
        for x in range(self.width):
            for y in range(self.height):
                tile_array[x, y] = tile_array[x, y].remove_borders()
        return tile_array

    def get_image(self, tile_array):
        image = []
        for y in range(tile_array.shape[1]):
            for line in range(8):
                for x in range(tile_array.shape[0]):
                    image.append(''.join(tile_array[x, y].tile_lines[line]))
                image.append('\n')
        return ''.join(image[:-1])

    def get_matching_sides(self, possible_tile_to_check, all_tiles):
        matching_sides = 0
        for tile in all_tiles:
            if tile.tile_number != possible_tile_to_check.tile_number:
                tile_all_borders = tile.get_all_borders()
                matching_sides += sum(1 for border in possible_tile_to_check.get_all_borders()
                                      if border in tile_all_borders)
        return matching_sides

    @functools.lru_cache(999)
    @Utils.listify(wrapper=tuple)
    def get_all_borders(self):
        for tile in self.get_all_tiles(only_flipped=True):
            yield from tile.get_all_borders()

    def get_borders_count(self):
        borders_count = collections.Counter()
        for border in self.get_all_borders():
            borders_count[border] += 1
        return borders_count

    @functools.lru_cache(999)
    @Utils.listify(wrapper=frozenset)
    def get_unique_borders(self):
        for border, border_count in self.get_borders_count().items():
            if border_count == 1:
                yield border

    @functools.lru_cache(999)
    @Utils.listify(wrapper=tuple)
    def get_corner_tiles(self):
        for tile, borders_counts in self.get_tiles_with_border_count():
            if sum(borders_count == 0 for borders_count in borders_counts) == 2:
                yield tile

    @Utils.listify(wrapper=tuple)
    def get_border_count(self, tile: Tile):
        borders_count = collections.Counter()
        for curr_tile in self.get_all_tiles(only_flipped=True):
            if curr_tile.tile_number != tile.tile_number:
                for border in curr_tile.get_all_borders():
                    borders_count[border] += 1
        for border in tile.get_all_borders():
            yield borders_count[border]

    @Utils.listify(wrapper=tuple)
    def get_tiles_with_border_count(self):
        for tile in self.get_all_tiles():
            yield tile, self.get_border_count(tile)

    @functools.lru_cache(999)
    def get_corner_tile_numbers(self):
        return frozenset(tile.tile_number for tile in self.get_corner_tiles())

    @functools.lru_cache(999)
    def get_all_tiles(self, only_flipped=False):
        return frozenset(possible_tiles for tile in self.tiles
                         for possible_tiles in tile.get_all_possible_tiles(only_flipped=only_flipped))

    def get_result_1st(self):
        return multiply(self.get_corner_tile_numbers())


def parse_input(my_input):
    return [Tile.parse_tile(tile_str) for tile_str in my_input.strip().split('\n\n')]


test_input_solver = TilesSolver(parse_input(TEST_INPUT))
assert test_input_solver.get_result_1st() == (1951 * 3079 * 2971 * 1171), \
    test_input_solver.get_result_1st()

test_input_solver.remove_wrong_possibilities()

image = test_input_solver.get_image(test_input_solver.remove_borders(test_input_solver.get_tile_array()))
print(image, '\n')

assert image.strip() == """
.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.##..
#.#.##.###.#.##.##.#####
..##.###.####..#.####.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.######.
.###.###.#######..#####.
..##.#..#..#.#######.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#
""".strip()

if False:
    image = '\n'.join(
        ''.join(line) for line in np.rot90(np.array([list(line) for line in image.strip().split('\n')]), k=-1))
    print(image, '\n')

    image = '\n'.join(''.join(line) for line in np.fliplr(np.array([list(line) for line in image.strip().split('\n')])))
    print(image, '\n')

image_replaced = re.sub(r'^(.*..................)#(..*\n)'
                        r'^(.*)#(....)##(....)##(....)###(.*\n)'
                        r'^(.*.)#(..)#(..)#(..)#(..)#(..)#(....*\n)',
                        '\g<1>O\g<2>\g<3>O\g<4>OO\g<5>OO\g<6>OOO\g<7>\g<8>O\g<9>O\g<10>O\g<11>O\g<12>O\g<13>O\g<14>',
                        image, flags=re.MULTILINE)

assert image_replaced.count('#') == 273

tiles_solver = TilesSolver(parse_input(PUZZLE_INPUT))
print(tiles_solver.get_result_1st())
# 64802175715999

tiles_solver.remove_wrong_possibilities()
image = tiles_solver.get_image(tiles_solver.remove_borders(tiles_solver.get_tile_array()))
image_replaced = re.sub(r'^(.*..................)#(..*\n)'
                        r'^(.*)#(....)##(....)##(....)###(.*\n)'
                        r'^(.*.)#(..)#(..)#(..)#(..)#(..)#(....*\n)',
                        '\g<1>O\g<2>\g<3>O\g<4>OO\g<5>OO\g<6>OOO\g<7>\g<8>O\g<9>O\g<10>O\g<11>O\g<12>O\g<13>O\g<14>',
                        image, flags=re.MULTILINE)

print(image_replaced.count('#'))

"""
.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.##..
#.#.##.###.#.##.##.#####
..##.###.####..#.####.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.######.
.###.###.#######..#####.
..##.#..#..#.#######.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#
"""
