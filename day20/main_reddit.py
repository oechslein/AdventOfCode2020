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


def turn(lines, turns):
    for x in range(turns):
        turn = []
        for y in range(len(lines)):
            turn.append(''.join([z[y] for z in reversed(lines)]))
        lines = [y for y in turn]
    return lines


data = {int(x.split(':\n')[0].split(' ')[1]): x.split(':\n')[1] for x in PUZZLE_INPUT.strip('\n').split('\n\n')}
all_borders_dict, all_tiles_dict = {}, {}
for tile_number, tiles in data.items():
    lines = tiles.split('\n')
    all_tiles_dict[tile_number] = [lines, turn(lines, 1), turn(lines, 2), turn(lines, 3), [x[::-1] for x in lines],
                                   turn([x[::-1] for x in lines], 1), turn([x[::-1] for x in lines], 2),
                                   turn([x[::-1] for x in lines], 3)]
    all_borders_dict[tile_number] = [tile[0] for tile in all_tiles_dict[tile_number]]
border_total_amount_dict = {tile_number: sum(1 for border in tile_borders
                                             if any(border in other_tile_borders
                                                    for other_tile_number, other_tile_borders in
                                                    all_borders_dict.items()
                                                    if tile_number != other_tile_number))
                            for tile_number, tile_borders in all_borders_dict.items()}
print('Part 1: {}'.format(Utils.multiply(tile_number
                                         for tile_number, border_total_amount in border_total_amount_dict.items()
                                         if border_total_amount == min(border_total_amount_dict.values()))))
picture = [[[] for x in range(int(len(data.keys()) ** 0.5))] for y in range(int(len(data.keys()) ** 0.5))]
used = []
for tile_number, tiles in all_tiles_dict.items():
    if border_total_amount_dict[tile_number] == min(border_total_amount_dict.values()):
        all_other_tile_borders = sum([other_tile_borders
                                      for other_tile_number, other_tile_borders in all_borders_dict.items()
                                      if tile_number != other_tile_number], [])
        for tile in all_tiles_dict[tile_number]:
            if ''.join([tile[-1] for tile in tile]) in all_other_tile_borders \
                    and tile[-1] in all_other_tile_borders:
                picture[0][0], used = tile, [tile_number]
                break
        if used:
            break
for y in range(len(picture)):
    if y == 0:
        for x in range(1, len(picture)):
            for key in all_tiles_dict.keys():
                if key not in used:
                    for i in range(len(all_tiles_dict[key])):
                        if ''.join([t[0] for t in all_tiles_dict[key][i]]) == ''.join(
                                [j[-1] for j in picture[y][x - 1]]):
                            picture[y][x] = all_tiles_dict[key][i]
                            used.append(key)

    else:
        for x in range(len(picture[0])):
            for key in all_tiles_dict.keys():
                if key not in used:
                    for i in range(len(all_tiles_dict[key])):
                        if all_tiles_dict[key][i][0] == picture[y - 1][x][-1]:
                            picture[y][x] = all_tiles_dict[key][i]
                            used.append(key)
for y in range(len(picture)):
    for x in range(len(picture)):
        picture[y][x] = [f[1:-1] for f in picture[y][x][1:-1]]
final = []
for y in picture:
    for x in range(len(y[0])):
        final.append(''.join([z[x] for z in y]))
dragon = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''.strip('\n').split('\n')
idx = []
for y in range(len(dragon)):
    for x in range(len(dragon[0])):
        if dragon[y][x] == '#':
            idx.append([x, y])
tot = 0
for rot in [final, turn(final, 1), turn(final, 2), turn(final, 3), [x[::-1] for x in final],
            turn([x[::-1] for x in final], 1), turn([x[::-1] for x in final], 2),
            turn([x[::-1] for x in final], 3)]:
    for y in range(len(final) - len(dragon)):
        for tile in range(len(rot[y]) - len(dragon[0])):
            if all([rot[y + j][tile + i] == '#' for i, j in idx]):
                tot += len([z for z in ''.join(dragon) if z == '#'])
print('Part 2: {}'.format(len([z for z in ''.join(final) if z == '#']) - tot))
