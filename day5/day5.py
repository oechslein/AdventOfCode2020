import itertools
from functools import reduce

from day5_input import puzzle_input


def bin_search(seat_code, range_value, low_range_marker, high_range_marker):
    def bin_search_rec(curr_seat_code, curr_range):
        if curr_seat_code == "":
            assert curr_range[0] == curr_range[1]
            return curr_range[0]
        elif curr_seat_code[0] == low_range_marker:
            return bin_search_rec(curr_seat_code[1:], (curr_range[0], (curr_range[0] + curr_range[1]) // 2))
        else:
            assert curr_seat_code[0] == high_range_marker
            return bin_search_rec(curr_seat_code[1:], ((curr_range[0] + curr_range[1]) // 2 + 1, curr_range[1]))

    return bin_search_rec(seat_code, range_value)


def find_seat_id(seat_code):
    row = bin_search(seat_code[0:7], (0, 127), "F", "B")
    column = bin_search(seat_code[7:10], (0, 7), "L", "R")
    return row * 8 + column


assert find_seat_id("FBFBBFFRLR") == (44, 5, 357)[2], find_seat_id("FBFBBFFRLR")
assert find_seat_id("BFFFBBFRRR") == (70, 7, 567)[2], find_seat_id("BFFFBBFRRR")
assert find_seat_id("FFFBBBFRRR") == (14, 7, 119)[2], find_seat_id("FFFBBBFRRR")
assert find_seat_id("BBFFBBFRLL") == (102, 4, 820)[2], find_seat_id("BBFFBBFRLL")

print(max(find_seat_id(seat_code) for seat_code in puzzle_input.strip().split('\n')))

#### 2nd

all_seat_ids = {row * 8 + column for row in range(0, 128) for column in range(0, 8)}
seat_ids_in_list = {find_seat_id(seat_code) for seat_code in puzzle_input.strip().split('\n')}
missing_seat_ids = all_seat_ids - seat_ids_in_list
possible_seat_ids = [missing_seat_id for missing_seat_id in missing_seat_ids
                     if (missing_seat_id - 1 in seat_ids_in_list) and (missing_seat_id + 1 in seat_ids_in_list)]
print(possible_seat_ids)


#### 1nd binär

def calc_seat_id(seat_code):
    return reduce(lambda prev, new: 2 * prev + {"F": 0, "B": 1, "L": 0, "R": 1}[new], seat_code, 0)


print(max(calc_seat_id(seat_code) for seat_code in puzzle_input.strip().split('\n')))

seat_ids_in_list = list(sorted(calc_seat_id(seat_code) for seat_code in puzzle_input.strip().split('\n')))
possible_seat_ids = [curr_seat + 1 for curr_seat, next_seat in zip(seat_ids_in_list, seat_ids_in_list[1:]) if next_seat != curr_seat + 1]
print(possible_seat_ids)
