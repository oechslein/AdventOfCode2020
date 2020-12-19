import re

from input import PUZZLE_INPUT, TEST_INPUT_2ND, TEST_INPUT


class alt_list(list):
    pass


class sequence_list(list):
    pass


"""
bbabbbbaabaabba: True and True [8, 42, 9, 14, 27, 14, 18, 15, 1, 15, 14, 14, 11, 42, 9, 14, 27, 14, 18, 15, 1, 15, 1, 14, 31, 1, 13, 1, 12, 19, 14, 14, 1]
ababaaaaaabaaab: True and True [8, 42, 10, 23, 25, 1, 14, 1, 14, 1, 11, 42, 10, 28, 16, 15, 1, 1, 1, 1, 1, 31, 14, 17, 1, 7, 1, 21, 1, 14]
ababaaaaabbbaba: True and True [8, 42, 10, 23, 25, 1, 14, 1, 14, 1, 11, 42, 9, 1, 26, 1, 20, 1, 15, 1, 14, 31, 14, 17, 14, 2, 1, 24, 14, 1]
"""


def parse_input(my_input, replace=True):
    rule_lines, test_lines = my_input.strip().split('\n\n')
    if replace:
        rule_lines = rule_lines.replace('8: 42', '8: 42 | 42 8').replace('11: 42 31', '11: 42 31 | 42 11 31')

    def make_alt_list(my_list):
        my_list = list(my_list)
        if len(my_list) == 1:
            return my_list[0]
        else:
            return alt_list(my_list)

    def make_sequence_list(my_list):
        my_list = list(my_list)
        if len(my_list) == 1:
            return my_list[0]
        else:
            return sequence_list(my_list)

    def parse_alternative(alternative):
        return make_sequence_list(
            int(elem) if re.fullmatch(r'\d+', elem) else elem[1] for elem in alternative.split(' '))

    def parse_rule_line(rule_line):
        result = re.fullmatch(r'(\d+): (.*)', rule_line)
        return int(result.group(1)), make_alt_list(parse_alternative(alternative)
                                                   for alternative in result.group(2).split(' | '))

    rules_dict = dict(parse_rule_line(rule_line) for rule_line in rule_lines.split('\n'))

    return rules_dict, test_lines.split('\n')


def restrict_possibilities(current_possibilities, test_line):
    return {(test_line_index, applied_rules) for test_line_index, applied_rules in current_possibilities
            if test_line_index < len(test_line)}


def match_rule_alt(current_possibilities, test_line, curr_rule, rules_dict):
    new_current_possibilities = set()
    for elem in curr_rule:
        new_current_possibilities.update(match_rule(current_possibilities, test_line, elem, rules_dict))
    return new_current_possibilities


def match_rule_seq(current_possibilities, test_line, curr_rule, rules_dict):
    for elem in curr_rule:
        current_possibilities = match_rule(current_possibilities, test_line, elem, rules_dict)
    return current_possibilities


def match_rule(current_possibilities, test_line, curr_rule, rules_dict):
    current_possibilities = restrict_possibilities(current_possibilities, test_line)
    if not current_possibilities:
        return current_possibilities
    if isinstance(curr_rule, sequence_list):
        return match_rule_seq(current_possibilities, test_line, curr_rule, rules_dict)
    elif isinstance(curr_rule, alt_list):
        return match_rule_alt(current_possibilities, test_line, curr_rule, rules_dict)
    elif isinstance(curr_rule, int):
        current_possibilities = {(test_line_index, applied_rules + (curr_rule,))
                                 for test_line_index, applied_rules in current_possibilities}
        return match_rule(current_possibilities, test_line, rules_dict[curr_rule], rules_dict)
    else:
        assert isinstance(curr_rule, str)
        return {(test_line_index + 1, applied_rules)
                for test_line_index, applied_rules in current_possibilities
                if curr_rule == test_line[test_line_index]}


def match_rule_first(index, test_line, rules_dict, with_print=False):
    current_possibilities = match_rule({(0, (0,))}, test_line, rules_dict[0], rules_dict)
    current_possibilities = {(test_line_index, applied_rules)
                             for test_line_index, applied_rules in current_possibilities
                             if test_line_index == len(test_line)}
    if with_print:
        print(f'{index} {test_line}: {current_possibilities}')
    return len(current_possibilities) > 0


def check(rules_dict, test_lines, with_print=False):
    return sum(1 for index, test_line in enumerate(test_lines)
               if match_rule_first(index, test_line, rules_dict, with_print=with_print))


assert check(*parse_input(TEST_INPUT, replace=False), with_print=True) == 2
assert check(*parse_input(TEST_INPUT_2ND, replace=False), with_print=True) == 3
print(check(*parse_input(PUZZLE_INPUT, replace=False), with_print=True))

assert not match_rule_first(0, "a", parse_input(TEST_INPUT_2ND)[0])
assert match_rule_first(0, "bbabbbbaabaabba", parse_input(TEST_INPUT_2ND)[0])
assert match_rule_first(0, "babbbbaabbbbbabbbbbbaabaaabaaa", parse_input(TEST_INPUT_2ND)[0])
assert not match_rule_first(0, "aaaabbaaaabbaaa", parse_input(TEST_INPUT_2ND)[0])
assert check(*parse_input(TEST_INPUT_2ND), with_print=True) == 12
print(check(*parse_input(PUZZLE_INPUT), with_print=True))
