from typing import List, Mapping, Dict

from input import TEST_INPUT, PUZZLE_INPUT, TEST_INPUT_2ND, PUZZLE_INPUT_2ND


def parse_input(my_input):
    return list(map(int, my_input.strip().split(',')))


def parse_input_2nd(my_input_list):
    return [(nth_number_spoken, list(map(int, number_str.strip().split(','))), result)
            for nth_number_spoken, number_str, result in my_input_list]


def get_number_spoken(nth_number_spoken: int, turns: List[int]):
    numbers_spoken: Dict[int, int] = {}
    curr_turn: int = 1
    for spoken_number in turns[:-1]:
        numbers_spoken[spoken_number] = curr_turn
        curr_turn += 1
    previous_spoken_number: int = turns[-1]
    while True:
        curr_turn += 1
        if curr_turn > nth_number_spoken:
            return previous_spoken_number
        # check if previous_spoken_number
        # - was never spoken => speak it
        # - was spoken => calc difference curr_turn - spoken_turn and speak it
        if previous_spoken_number not in numbers_spoken:
            numbers_spoken[previous_spoken_number] = curr_turn - 1
            previous_spoken_number = 0
        else:
            new_number = (curr_turn - 1) - numbers_spoken[previous_spoken_number]
            numbers_spoken[previous_spoken_number] = curr_turn - 1
            previous_spoken_number = new_number


assert get_number_spoken(2020, parse_input(TEST_INPUT)) == 436
print(get_number_spoken(2020, parse_input(PUZZLE_INPUT)))


def check_2nd_input(my_input):
    for nth_number_spoken, number_str, result in my_input:
        calc_result = get_number_spoken(nth_number_spoken, number_str)
        if result is not None:
            assert calc_result == result, (nth_number_spoken, number_str, result, calc_result)
        else:
            print(nth_number_spoken, number_str, calc_result)


check_2nd_input(parse_input_2nd(TEST_INPUT_2ND))
check_2nd_input(parse_input_2nd(PUZZLE_INPUT_2ND))
