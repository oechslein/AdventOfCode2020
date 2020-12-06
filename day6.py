from functools import reduce
from itertools import count

from day6_input import puzzle_input

test_input1 = """
abcx
abcy
abcz
"""

test_input2 = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""

def gen_group_input(my_input):
    return my_input.strip().split('\n\n')




def get_count(group_input):
    return len(set(char for char in group_input.replace('\n', '')))


def get_sum_counts(my_input):
    return sum(get_count(group_input) for group_input in gen_group_input(my_input))


assert get_sum_counts(test_input1) == 6

assert get_sum_counts(test_input2) == 11

print(get_sum_counts(puzzle_input))


## part 2

def combine(all_answers_set, person_answers_set):
    if all_answers_set is None:
        return person_answers_set
    else:
        return all_answers_set.intersection(person_answers_set)


def gen_answer_sets(group_input):
    return (set(answer for answer in person_str) for person_str in group_input.split('\n'))


def get_group_count(group_input):
    return len(reduce(combine, gen_answer_sets(group_input), None))


def get_group_sum_counts(my_input):
    return sum(get_group_count(group_input) for group_input in gen_group_input(my_input))


assert get_group_sum_counts(test_input2) == 6

print(get_group_sum_counts(puzzle_input))
