import functools
import math
import re

from frozendict import frozendict

import Utils
from input import PUZZLE_INPUT, TEST_INPUT


class TileSolver(object):
    def __init__(self, my_input):
        self.used_tile_numbers = []
        self.data = TileSolver.parse_input(my_input)
        self.width = math.isqrt(len(self.data))
        self.picture = [[[] for x in range(self.width)] for y in range(self.width)]

    @staticmethod
    def turn(lines, turns):
        for x in range(turns):
            turn = []
            for y in range(len(lines)):
                turn.append(''.join([z[y] for z in reversed(lines)]))
            lines = [y for y in turn]
        return lines

    @staticmethod
    def flip(lines):
        return [x[::-1] for x in lines]

    @staticmethod
    def parse_input(my_input):
        return frozendict({int(tile_data.split(':\n')[0].split(' ')[1]): tuple(tile_data.split(':\n')[1].split('\n'))
                           for tile_data in my_input.strip('\n').split('\n\n')})

    @staticmethod
    def create_all_possible_tiles(tile):
        return (tile, TileSolver.turn(tile, 1), TileSolver.turn(tile, 2),
                TileSolver.turn(tile, 3), TileSolver.flip(tile),
                TileSolver.turn(TileSolver.flip(tile), 1),
                TileSolver.turn(TileSolver.flip(tile), 2),
                TileSolver.turn(TileSolver.flip(tile), 3))

    @functools.lru_cache(999)
    def get_all_tiles_dict(self):
        return frozendict({tile_number: self.create_all_possible_tiles(tile)
                           for tile_number, tile in self.data.items()})

    @functools.lru_cache(999)
    def get_all_borders_dict(self):
        return frozendict({tile_number: tuple(self.get_south_border(tile) for tile in tiles)
                           for tile_number, tiles in self.get_all_tiles_dict().items()})

    @functools.lru_cache(999)
    def get_border_total_amount_dict(self):
        return {tile_number: sum(1 for border in tile_borders
                                 if any(border in other_tile_borders
                                        for other_tile_number, other_tile_borders in self.get_all_borders_dict().items()
                                        if tile_number != other_tile_number))
                for tile_number, tile_borders in self.get_all_borders_dict().items()}

    def calc_1st(self):
        border_total_amount_dict = self.get_border_total_amount_dict()
        return Utils.multiply(tile_number
                              for tile_number, border_total_amount in border_total_amount_dict.items()
                              if border_total_amount == min(border_total_amount_dict.values()))

    def get_left_upper_corner_tile(self):
        min_border_amount = min(self.get_border_total_amount_dict().values())
        min_tile_numbers = {tile_number: tiles
                            for tile_number, tiles in self.get_all_tiles_dict().items()
                            if self.get_border_total_amount_dict()[tile_number] == min_border_amount}
        for tile_number, tiles in min_tile_numbers.items():
            other_tile_borders_set = {
                other_tile_borders
                for other_tile_number, other_tile_borders in self.get_all_borders_dict().items()
                if tile_number != other_tile_number}
            all_other_tile_borders = functools.reduce(set.union, other_tile_borders_set, set())

            for tile in tiles:
                # check if right east and north borders exist
                if self.get_east_border(tile) in all_other_tile_borders \
                        and self.get_north_border(tile) in all_other_tile_borders:
                    return tile_number, tile
        assert False

    @staticmethod
    def get_north_border(tile):
        return tile[-1]

    @staticmethod
    def get_south_border(tile):
        return tile[0]

    @staticmethod
    def get_west_border(tile):
        return ''.join(subtile[0] for subtile in tile)

    @staticmethod
    def get_east_border(tile):
        return ''.join(subtile[-1] for subtile in tile)

    def set_left_upper_corner_tile(self):
        tile_number, tile = self.get_left_upper_corner_tile()
        self.picture[0][0] = tile
        self.used_tile_numbers = [tile_number]

    def gen_all_flatten_tiles(self):
        for tile_number, tiles in self.get_all_tiles_dict().items():
            if tile_number not in self.used_tile_numbers:
                for tile in tiles:
                    yield tile_number, tile

    def set_first_row(self):
        y = 0
        # start with 1 since 0 already set!
        for x in range(1, self.width):
            for tile_number, tile in self.gen_all_flatten_tiles():
                if self.get_west_border(tile) == self.get_east_border(self.picture[y][x - 1]):
                    self.picture[y][x] = tile
                    self.used_tile_numbers.append(tile_number)
                    break

    def set_remaining_rows(self):
        for y in range(1, self.width):
            for x in range(self.width):
                for tile_number, tile in self.gen_all_flatten_tiles():
                    if self.get_south_border(tile) == self.get_north_border(self.picture[y - 1][x]):
                        if x != 0:
                            assert self.get_west_border(tile) == self.get_east_border(self.picture[y][x - 1])
                        self.picture[y][x] = tile
                        self.used_tile_numbers.append(tile_number)
                        break

    def solve(self):
        self.set_left_upper_corner_tile()
        self.set_first_row()
        self.set_remaining_rows()

    def get_final_picture(self):
        final = []
        for y in range(self.width):
            for x in range(len(self.picture[y][0])):
                final.append(''.join([row[x] for row in self.picture[y]]))
        return final

    def cut_other_borders(self):
        for y in range(self.width):
            for x in range(self.width):
                self.picture[y][x] = [tile_row[1:-1] for tile_row in self.picture[y][x][1:-1]]

    @functools.lru_cache(999)
    def get_dragon(self):
        return ['                  # ',
                '#    ##    ##    ###',
                ' #  #  #  #  #  #   ']

    def get_sea_dragon_indexes(self, dragon):
        idx = []
        for y in range(len(dragon)):
            for x in range(len(dragon[0])):
                if dragon[y][x] == '#':
                    idx.append([x, y])
        return idx

    def get_sea_dragon_count_old(self, final_picture):
        dragon = self.get_dragon()
        idx = self.get_sea_dragon_indexes(dragon)
        sea_dragon_count = 0
        for final_picture in TileSolver.create_all_possible_tiles(final_picture):
            for y in range(len(final_picture) - len(dragon)):
                for x in range(len(final_picture[y]) - len(dragon[0])):
                    if all([final_picture[y + j][x + i] == '#' for i, j in idx]):
                        sea_dragon_count += 1
        return sea_dragon_count

    def get_sea_dragon_count(self, final_picture):
        tot = 0
        for final_picture in TileSolver.create_all_possible_tiles(final_picture):
            image = '\n'.join(final_picture)
            seadragon_hashes = ['O', 'O', 'OO', 'OO', 'OOO', 'O', 'O', 'O', 'O', 'O', 'O']
            image_replaced = re.sub(
                r'^(.*..................)#(:?..*\n)'
                r'^(.*)#(....)##(....)##(....)###(:?.*\n)'
                r'^(.*.)#(..)#(..)#(..)#(..)#(..)#(:?....*\n)',
                ''.join(f'g<{i + 1}>{o_s}' for i, o_s in zip(range(len(seadragon_hashes)), seadragon_hashes)),
                image, flags=re.MULTILINE)

            tot += image_replaced.count('O') // ''.join(self.get_dragon()).count('#')
        return tot

    def calc_2nd(self):
        self.solve()
        self.cut_other_borders()
        final_picture = self.get_final_picture()
        sea_dragon_count = self.get_sea_dragon_count(final_picture)
        sea_dragon_count_old = self.get_sea_dragon_count_old(final_picture)
        assert sea_dragon_count == sea_dragon_count_old
        return ''.join(final_picture).count('#') - sea_dragon_count * ''.join(self.get_dragon()).count('#')


tile_solver = TileSolver(TEST_INPUT)
assert tile_solver.calc_1st() == (1951 * 3079 * 2971 * 1171)
assert tile_solver.calc_2nd() == 273

############################################################################################################

tile_solver = TileSolver(PUZZLE_INPUT)
part_1 = tile_solver.calc_1st()
print('Part 1: {}'.format(part_1))

part_2 = tile_solver.calc_2nd()
print('Part 2: {}'.format(part_2))

assert part_1 == 64802175715999
assert part_2 == 2146
