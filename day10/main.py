import collections
import time

import numpy as np

from Utils import multiply
from input import TEST_INPUT, TEST_INPUT_2, PUZZLE_INPUT


def parse_input(my_input):
    return list(sorted(int(adapter) for adapter in my_input.strip().split('\n')))


def get_jolt_differences(adapter_list):
    def get_jolt_differences_rec(curr_adapter, remaining_adapter_list, sorted_adapter_list):
        if len(remaining_adapter_list) == 0:
            return sorted_adapter_list + [(curr_adapter + 3, 3)]
        else:
            for index, next_adapter in enumerate(remaining_adapter_list):
                jolt_difference = next_adapter - curr_adapter
                if 1 <= jolt_difference <= 3:
                    result = get_jolt_differences_rec(next_adapter, remaining_adapter_list[0:index] + remaining_adapter_list[index + 1:],
                                                      sorted_adapter_list + [(curr_adapter, jolt_difference)])
                    if result:
                        return result
            # nothing found
            return None

    sorted_adapter_list = get_jolt_differences_rec(0, adapter_list, [])
    assert sorted_adapter_list is not None

    jolt_differences = collections.Counter()
    for curr_adapter, jolt_difference in sorted_adapter_list:
        jolt_differences[jolt_difference] += 1

    return jolt_differences


def get_jolt_differences_number(adapter_list):
    jolt_differences = get_jolt_differences(adapter_list)
    return jolt_differences[1] * jolt_differences[3]


assert get_jolt_differences_number(parse_input(TEST_INPUT)) == (7 * 5)

assert get_jolt_differences_number(parse_input(TEST_INPUT_2)) == (22 * 10)

print(get_jolt_differences_number(parse_input(PUZZLE_INPUT)))


# 2nd

def get_all_jolt_combinations(adapter_list):
    def get_jolt_differences_rec(curr_adapter, remaining_adapter_list, sorted_adapter_list):
        if len(remaining_adapter_list) == 0:
            return [sorted_adapter_list + [curr_adapter, curr_adapter + 3]]
        else:
            all_correct_results = []
            for index, next_adapter in enumerate(remaining_adapter_list):
                jolt_difference = next_adapter - curr_adapter
                if 1 <= jolt_difference <= 3:
                    all_correct_sub_results = get_jolt_differences_rec(next_adapter, remaining_adapter_list[index + 1:],
                                                                       sorted_adapter_list + [curr_adapter])
                    all_correct_results.extend(all_correct_sub_results)
            return all_correct_results

    all_correct_results = get_jolt_differences_rec(0, adapter_list, [])
    return set(tuple(correct_result) for correct_result in all_correct_results)


TEST_INPUT_ARRANGEMENTS = {
    (0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22),
    (0, 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, 22),
    (0, 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, 22),
    (0, 1, 4, 5, 7, 10, 12, 15, 16, 19, 22),
    (0, 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, 22),
    (0, 1, 4, 6, 7, 10, 12, 15, 16, 19, 22),
    (0, 1, 4, 7, 10, 11, 12, 15, 16, 19, 22),
    (0, 1, 4, 7, 10, 12, 15, 16, 19, 22),
}


def get_jolt_combination_amount_slow(adapter_list, start_adapter):
    adapter_list = np.array(adapter_list)
    adapter_list_len = len(adapter_list)

    def get_jolt_differences_rec(curr_adapter, index_adapter_list):
        if index_adapter_list == adapter_list_len:
            return 1
        else:
            all_correct_results = 0
            for index in range(index_adapter_list, len(adapter_list)):
                next_adapter = adapter_list[index]
                jolt_difference = next_adapter - curr_adapter
                if 1 <= jolt_difference <= 3:
                    all_correct_results += get_jolt_differences_rec(next_adapter, index + 1)
                if jolt_difference >= 4:
                    # it is sorted...
                    break
            return all_correct_results

    return get_jolt_differences_rec(start_adapter, 0)


def split_in_3_jump_groups(adapter_list):
    curr_group = [0]
    curr_adapter = 0
    for adapter in adapter_list:
        if adapter - curr_adapter == 3:
            yield curr_group
            curr_group = []
        curr_adapter = adapter
        curr_group.append(curr_adapter)
    yield curr_group


def get_jolt_combination_amount_fast(my_input):
    x = [(len(adapter_list),
          (pow(2, len(adapter_list) - 2) if len(adapter_list) > 2 else 1),
          get_jolt_combination_amount_slow(adapter_list[1:], adapter_list[0]), adapter_list)
         for adapter_list in split_in_3_jump_groups(parse_input(my_input))]


    new_sum = multiply((pow(2, len(adapter_list)-2) if len(adapter_list) > 2 else 1)
                       for adapter_list in split_in_3_jump_groups(parse_input(my_input)))
    old_sum = multiply([get_jolt_combination_amount_slow(adapter_list[1:], adapter_list[0])
                     for adapter_list in split_in_3_jump_groups(parse_input(my_input))])
    assert old_sum == new_sum
    return old_sum


for adapter_list in [list(range(i)) for i in range(2, 30)]:
    print(max(adapter_list), get_jolt_combination_amount_slow(adapter_list[1:], adapter_list[0]))


start_time = time.time()
assert get_all_jolt_combinations(parse_input(TEST_INPUT)) == TEST_INPUT_ARRANGEMENTS
assert len(get_all_jolt_combinations(parse_input(TEST_INPUT))) == 8
assert len(get_all_jolt_combinations(parse_input(TEST_INPUT_2))) == 19208
print(f'time get_all_jolt_combinations: {time.time() - start_time}')

start_time = time.time()
assert get_jolt_combination_amount_slow(parse_input(TEST_INPUT), 0) == 8
assert get_jolt_combination_amount_slow(parse_input(TEST_INPUT_2), 0) == 19208
print(f'time get_jolt_combination_amount_slow: {time.time() - start_time}')

start_time = time.time()
assert get_jolt_combination_amount_fast(TEST_INPUT) == 8
assert get_jolt_combination_amount_fast(TEST_INPUT_2) == 19208
print(f'time get_jolt_combination_amount_fast: {time.time() - start_time}')

print(get_jolt_combination_amount_fast(PUZZLE_INPUT))
