import functools

from frozendict import frozendict

import Utils
from input import PUZZLE_INPUT


class TileSolver(object):
    def __init__(self, my_input):
        self.data = TileSolver.parse_input(my_input)
        self.width = int(len(self.data.keys()) ** 0.5)

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

    @functools.lru_cache(999)
    def get_all_tiles_dict(self):
        all_tiles_dict = {}
        for tile_number, lines in self.data.items():
            all_tiles_dict[tile_number] = (lines, TileSolver.turn(lines, 1), TileSolver.turn(lines, 2),
                                           TileSolver.turn(lines, 3), TileSolver.flip(lines),
                                           TileSolver.turn(TileSolver.flip(lines), 1),
                                           TileSolver.turn(TileSolver.flip(lines), 2),
                                           TileSolver.turn(TileSolver.flip(lines), 3))
        return frozendict(all_tiles_dict)

    @functools.lru_cache(999)
    def get_all_borders_dict(self):
        all_borders_dict = {}
        for tile_number in self.get_all_tiles_dict():
            all_borders_dict[tile_number] = [tile[0] for tile in self.get_all_tiles_dict()[tile_number]]
        return all_borders_dict

    @functools.lru_cache(999)
    def get_border_total_amount_dict(self):
        return {tile_number: sum(1 for border in tile_borders
                                 if any(border in other_tile_borders
                                        for other_tile_number, other_tile_borders in self.get_all_borders_dict().items()
                                        if tile_number != other_tile_number))
                for tile_number, tile_borders in self.get_all_borders_dict().items()}

    def calc_part_1(self):
        border_total_amount_dict = self.get_border_total_amount_dict()
        return Utils.multiply(tile_number
                              for tile_number, border_total_amount in border_total_amount_dict.items()
                              if border_total_amount == min(border_total_amount_dict.values()))

    def calc_2nd(self):
        picture = [[[] for x in range(self.width)] for y in range(self.width)]
        used = []
        for tile_number, tiles in self.get_all_tiles_dict().items():
            if self.get_border_total_amount_dict()[tile_number] == min(self.get_border_total_amount_dict().values()):
                all_other_tile_borders = sum([other_tile_borders
                                              for other_tile_number, other_tile_borders in
                                              self.get_all_borders_dict().items()
                                              if tile_number != other_tile_number], [])
                for tile in self.get_all_tiles_dict()[tile_number]:
                    if ''.join([tile[-1] for tile in tile]) in all_other_tile_borders \
                            and tile[-1] in all_other_tile_borders:
                        picture[0][0], used = tile, [tile_number]
                        break
                if used:
                    break
        for y in range(len(picture)):
            if y == 0:
                for x in range(1, len(picture)):
                    for key in self.get_all_tiles_dict().keys():
                        if key not in used:
                            for i in range(len(self.get_all_tiles_dict()[key])):
                                if ''.join([t[0] for t in self.get_all_tiles_dict()[key][i]]) == ''.join(
                                        [j[-1] for j in picture[y][x - 1]]):
                                    picture[y][x] = self.get_all_tiles_dict()[key][i]
                                    used.append(key)

            else:
                for x in range(len(picture[0])):
                    for key in self.get_all_tiles_dict().keys():
                        if key not in used:
                            for i in range(len(self.get_all_tiles_dict()[key])):
                                if self.get_all_tiles_dict()[key][i][0] == picture[y - 1][x][-1]:
                                    picture[y][x] = self.get_all_tiles_dict()[key][i]
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
        for rot in [final, TileSolver.turn(final, 1), TileSolver.turn(final, 2), TileSolver.turn(final, 3),
                    TileSolver.flip(final),
                    TileSolver.turn(TileSolver.flip(final), 1), TileSolver.turn(TileSolver.flip(final), 2),
                    TileSolver.turn(TileSolver.flip(final), 3)]:
            for y in range(len(final) - len(dragon)):
                for tile in range(len(rot[y]) - len(dragon[0])):
                    if all([rot[y + j][tile + i] == '#' for i, j in idx]):
                        tot += len([z for z in ''.join(dragon) if z == '#'])
        part_2 = len([z for z in ''.join(final) if z == '#']) - tot
        return part_2


tile_solver = TileSolver(PUZZLE_INPUT)
part_1 = tile_solver.calc_part_1()
print('Part 1: {}'.format(part_1))

part_2 = tile_solver.calc_2nd()
print('Part 2: {}'.format(part_2))

assert part_1 == 64802175715999
assert part_2 == 2146
