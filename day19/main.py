import re

from input import PUZZLE_INPUT, TEST_INPUT


class alt_list(list):
    pass


class sequence_list(list):
    pass


def parse_input(my_input):
    rule_lines, test_lines = my_input.strip().split('\n\n')

    def parse_alternative(alternative):
        alternative_list = [int(elem) if re.fullmatch(r'\d+', elem) else elem[1] for elem in alternative.split(' ')]
        if len(alternative_list) == 1:
            return alternative_list[0]
        return sequence_list(alternative_list)

    def parse_rule_line(rule_line):
        result = re.fullmatch(r'(\d+): (.*)', rule_line)
        return int(result.group(1)), alt_list(parse_alternative(alternative)
                                              for alternative in result.group(2).split(' | '))

    rules_dict = dict(parse_rule_line(rule_line) for rule_line in rule_lines.split('\n'))

    return rules_dict, test_lines.split('\n')


def get_multiple_index(curr_elem, index_list):
    if not index_list:
        return curr_elem
    else:
        return get_multiple_index(curr_elem[index_list[0]], index_list[1:])


def set_multiple_index(curr_elem, index_list, value):
    assert index_list
    if len(index_list) == 1:
        curr_elem[index_list[0]] = value
    else:
        return set_multiple_index(curr_elem[index_list[0]], index_list[1:], value)


def expand_rules(rules_dict):
    def expand_rules_inner(curr_rule, index_list):
        for index, elem in enumerate(get_multiple_index(curr_rule, index_list)):
            if isinstance(elem, int):
                set_multiple_index(curr_rule, index_list + [index], rules_dict[elem])
                return True
            elif isinstance(elem, str):
                pass
            else:
                assert isinstance(elem, list), type(elem)
                if expand_rules_inner(curr_rule, index_list + [index]):
                    return True
        return False

    def remove_unnecessary_pars(elem_or_list):
        if isinstance(elem_or_list, list):
            if len(elem_or_list) == 1:
                return remove_unnecessary_pars(elem_or_list[0])
            else:
                mapped = map(remove_unnecessary_pars, elem_or_list)
                if isinstance(elem_or_list, alt_list):
                    return alt_list(mapped)
                else:
                    assert isinstance(elem_or_list, sequence_list)
                    return sequence_list(mapped)
        else:
            return elem_or_list

    while expand_rules_inner(rules_dict[0], []):
        pass
    return remove_unnecessary_pars(rules_dict[0])


def match_rule_alt(test_line, test_line_index, curr_rule):
    for elem in curr_rule:
        result, new_test_line_index = match_rule(test_line, test_line_index, elem)
        if result:
            return True, new_test_line_index
    return False, test_line_index


def match_rule_seq(test_line, test_line_index, curr_rule):
    for curr_rule in curr_rule:
        result, test_line_index = match_rule(test_line, test_line_index, curr_rule)
        if not result:
            return False, test_line_index
    return True, test_line_index


def match_rule(test_line, test_line_index, curr_rule):
    if isinstance(curr_rule, sequence_list):
        return match_rule_seq(test_line, test_line_index, curr_rule)
    elif isinstance(curr_rule, alt_list):
        return match_rule_alt(test_line, test_line_index, curr_rule)
    else:
        assert isinstance(curr_rule, str)
        return curr_rule == test_line[test_line_index], test_line_index + 1


def match_rule_first(test_line, test_line_index, expanded_rule):
    result, test_line_index = match_rule(test_line, test_line_index, expanded_rule)
    return result and test_line_index == len(test_line)


def check(rules_dict, test_lines):
    expanded_rule = expand_rules(rules_dict)
    return sum(1 for test_line in test_lines if match_rule_first(test_line, 0, expanded_rule))


assert check(*parse_input(TEST_INPUT)) == 2
print(check(*parse_input(PUZZLE_INPUT)))

# [[4, 1, 5]]
# [["a", 1, 5]]
