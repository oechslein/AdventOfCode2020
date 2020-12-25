import abc
import cProfile
import collections
import functools
import itertools
import operator
import time
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, List, Optional, ClassVar

import numpy as np

import Utils
from Utils import multiply, count
from input import PUZZLE_INPUT

import sys

import re


@dataclass
class Tile(object):
    x: int
    y: int
    white: bool = True
    NEIGHBOR_MAP: ClassVar[Dict[str, Tuple[int, int]]] = {'e': (+2, 0), 'se': (+1, -1), 'sw': (-1, -1),
                                                          'w': (-2, 0), 'nw': (-1, +1), 'ne': (+1, +1)}

    def __hash__(self):
        return self.x*13*7*11+self.y

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        else:
            return (self.x, self.y) == (other.x, other.y)

    def flip(self):
        self.white = not self.white

    @property
    def black(self):
        return not self.white

    def gen_neighbors(self):
        for direction, (x_diff, y_diff) in Tile.NEIGHBOR_MAP.items():
            yield self.x + x_diff, self.y + y_diff

    def get_neighbor_for_list(self, directions: List[str]):
        x, y = self.x, self.y
        for direction in directions:
            x_diff, y_diff = Tile.NEIGHBOR_MAP[direction]
            x += x_diff
            y += y_diff
        return x, y

    def need_flip(self, all_tiles: Dict[Tuple[int, int], "Tile"]):
        black_neighbors = self.black_neighbors_amount(all_tiles)
        if self.white:
            return 2 == black_neighbors
        else:
            return 0 == black_neighbors or black_neighbors > 2

    def black_neighbors_amount(self, all_tiles):
        return sum(all_tiles[(neighbor_x, neighbor_y)].black
                   for neighbor_x, neighbor_y in self.gen_neighbors()
                   if (neighbor_x, neighbor_y) in all_tiles)


def parse_line(line):
    mapping = {"se": "x", "sw": "y", "nw": "a", "ne": "b", "w": "w", "e": "e"}
    reverse_map = {exchange: direction for direction, exchange in mapping.items()}
    for direction, exchange in mapping.items():
        line = line.replace(direction, exchange)
    return [reverse_map[direction] for direction in line]


def parse_input(my_input: str):
    return [parse_line(line) for line in my_input.strip().split('\n')]


def get_all_tiles(directions_list):
    reference_tile = Tile(0, 0)
    all_tiles = {(0, 0): reference_tile}
    assert reference_tile.get_neighbor_for_list(["nw", "w", "sw", "e", "e"]) == (0, 0)
    for directions in directions_list:
        x, y = reference_tile.get_neighbor_for_list(directions)
        if (x, y) in all_tiles:
            all_tiles[(x, y)].flip()
        else:
            all_tiles[(x, y)] = Tile(x, y, False)
    return all_tiles


def count_blacks(all_tiles):
    return sum(tile.black for tile in all_tiles.values())


def calc1st(directions_list: List[List[str]]):
    return count_blacks(get_all_tiles(directions_list))


def calc2nd(directions_list: List[List[str]]):
    all_tiles = get_all_tiles(directions_list)
    for day in range(100):
        # Add missing whites
        for tile in list(all_tiles.values()):
            if tile.black:
                for neighbor_x, neighbor_y in tile.gen_neighbors():
                    if (neighbor_x, neighbor_y) not in all_tiles:
                        all_tiles[(neighbor_x, neighbor_y)] = Tile(neighbor_x, neighbor_y)

        tiles_to_flip = [tile for tile in all_tiles.values() if tile.need_flip(all_tiles)]
        for tile in tiles_to_flip:
            tile.flip()

        for tile in list(all_tiles.values()):
            if tile.white and tile.black_neighbors_amount(all_tiles) == 0:
                del all_tiles[(tile.x, tile.y)]

    print(count_blacks(all_tiles))
    return count_blacks(all_tiles)


TEST_INPUT = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""

start_time = time.time()
assert calc2nd(parse_input(TEST_INPUT)) == 2208
print(f'Duration: {time.time() - start_time}, {(time.time() - start_time) / 100} per round')
# Duration: 6.704365015029907, 0.06704365015029908 per round
# no print: Duration: 6.323774576187134, 0.06323774576187134 per round

print(calc2nd(parse_input(PUZZLE_INPUT)))
