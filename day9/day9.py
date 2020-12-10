from collections import namedtuple

from day9_input import TEST_INPUT, PUZZLE_INPUT

instruction_type = namedtuple("instruction_type", ["opp", "arg"])


def parse_input(my_input):
    return list(map(int, my_input.strip().split('\n')))


def gen_number_combinations(number_list):
    for index_x, x in enumerate(number_list):
        for index_y, y in enumerate(number_list):
            if index_x != index_y:
                assert x != y
                yield x, y


def find_number(number_to_find, number_list):
    for x, y in gen_number_combinations(number_list):
        if number_to_find == x + y:
            return True
    return False


def check_numbers(number_list, lookback_amount):
    for index in range(len(number_list) - lookback_amount):
        number_to_find = number_list[index + lookback_amount]
        if not find_number(number_to_find, number_list[index:lookback_amount + index]):
            return number_to_find


assert check_numbers(parse_input(TEST_INPUT), 5) == 127, check_numbers(parse_input(TEST_INPUT), 5)

print(check_numbers(parse_input(PUZZLE_INPUT), 25))


# 2089807806


## 2nd

def get_number_set(number_list, lookback_amount):
    number_to_find = check_numbers(number_list, lookback_amount)
    start_index = 0
    end_index = start_index + 2
    while True:
        part_of_number_list = number_list[start_index:end_index]
        sum_part_of_number_list = sum(part_of_number_list)
        if sum_part_of_number_list == number_to_find:
            return min(part_of_number_list) + max(part_of_number_list)
        elif sum_part_of_number_list > number_to_find:
            # cannot work, try next start_index
            start_index += 1
            end_index = start_index + 2
        else:
            end_index += 1


assert get_number_set(parse_input(TEST_INPUT), 5) == (15 + 47), get_number_set(parse_input(TEST_INPUT), 5)

print(get_number_set(parse_input(PUZZLE_INPUT), 25))
# 245848639
