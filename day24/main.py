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

    def flip(self):
        self.white = not self.white

    @property
    def black(self):
        return not self.white

    def gen_neighbors(self):
        for direction, (x_diff, y_diff) in Tile.NEIGHBOR_MAP.items():
            yield self.x + x_diff, self.y + y_diff

    def get_neighbor(self, direction: str):
        x_diff, y_diff = Tile.NEIGHBOR_MAP[direction]
        return self.x + x_diff, self.y + y_diff

    def get_neighbor_for_list(self, directions: List[str]):
        x, y = self.x, self.y
        for direction in directions:
            x_diff, y_diff = Tile.NEIGHBOR_MAP[direction]
            x += x_diff
            y += y_diff
        return x, y

def parse_line(line):
    mapping = {"se": "x", "sw": "y", "nw": "a", "ne": "b", "w": "w", "e": "e"}
    reverse_map = {exchange: direction for direction, exchange in mapping.items()}
    for direction, exchange in mapping.items():
        line = line.replace(direction, exchange)
    return [reverse_map[direction] for direction in line]

def parse_input(my_input: str):
    return [parse_line(line) for line in my_input.strip().split('\n')]


assert parse_line("sesenwnene") == ["se", "se", "nw", "ne", "ne"]

assert parse_line("wwwnwsenwnwnwnwnwnewnewsewnwnwnww") == ["w", "w", "w", "nw", "se", "nw", "nw", "nw", "nw", "nw",
                                                           "ne", "w", "ne", "w", "se", "w", "nw", "nw", "nw", "w"]



def calc(directions_list: List[List[str]]):
    reference_tile = Tile(0, 0)
    all_tiles = {(0, 0): reference_tile}
    assert reference_tile.get_neighbor_for_list(["nw", "w", "sw", "e", "e"]) == (0, 0)
    for directions in directions_list:
        x, y = reference_tile.get_neighbor_for_list(directions)
        if (x, y) in all_tiles:
            all_tiles[(x, y)].flip()
        else:
            all_tiles[(x, y)] = Tile(x, y, False)
    return sum(tile.black for tile in all_tiles.values())

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

assert calc(parse_input(TEST_INPUT)) == 10

print(calc(parse_input(PUZZLE_INPUT)))
