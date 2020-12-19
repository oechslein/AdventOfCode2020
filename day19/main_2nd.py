import re
from functools import lru_cache

from input import PUZZLE_INPUT, TEST_INPUT_2ND, TEST_INPUT


class sequence_list(list):
    pass


def parse_input(my_input, replace=True):
    rule_lines, test_lines = my_input.strip().split('\n\n')
    if replace:
        rule_lines = rule_lines.replace('8: 42', '8: 42 | 42 8').replace('11: 42 31', '11: 42 31 | 42 11 31')

    def parse_alternative(alternative):
        return [int(elem) if re.fullmatch(r'\d+', elem) else elem[1] for elem in alternative.split(' ')]

    def parse_rule_line(rule_line):
        result = re.fullmatch(r'(\d+): (.*)', rule_line)
        return int(result.group(1)), [parse_alternative(alternative)
                                      for alternative in result.group(2).split(' | ')]

    rules_dict = dict(parse_rule_line(rule_line) for rule_line in rule_lines.split('\n'))

    return rules_dict, test_lines.split('\n')


class GrammarChecker(object):
    def __init__(self, rules_dict):
        self.rules_dict = rules_dict

    @staticmethod
    def restrict_possibilities(current_possibilities, test_line):
        return {(test_line_index, applied_rules)
                for test_line_index, applied_rules in current_possibilities
                if test_line_index < len(test_line)}

    def match_rule_alt(self, current_possibilities, test_line, curr_rule):
        current_possibilities = self.restrict_possibilities(current_possibilities, test_line)
        if not current_possibilities:
            return current_possibilities
        new_current_possibilities = set()
        for elem in curr_rule:
            new_current_possibilities.update(self.match_rule_seq(current_possibilities, test_line, elem))
        return new_current_possibilities

    def match_rule_seq(self, current_possibilities, test_line, curr_rule):
        for elem in curr_rule:
            if isinstance(elem, int):
                current_possibilities = self.match_rule_int(current_possibilities, test_line, elem)
            else:
                assert isinstance(elem, str)
                current_possibilities = self.match_rule_str(current_possibilities, test_line, elem)
        return current_possibilities

    def match_rule_str(self, current_possibilities, test_line, curr_rule):
        current_possibilities = self.restrict_possibilities(current_possibilities, test_line)
        if not current_possibilities:
            return current_possibilities
        return {(test_line_index + 1, applied_rules)
                for test_line_index, applied_rules in current_possibilities
                if curr_rule == test_line[test_line_index]}

    def match_rule_int(self, current_possibilities, test_line, curr_rule):
        current_possibilities = {(test_line_index, applied_rules + (curr_rule,))
                                 for test_line_index, applied_rules in current_possibilities}
        return self.match_rule_alt(current_possibilities, test_line, self.rules_dict[curr_rule])

    def match_rule_first(self, index, test_line, with_print=False):
        possibilities = self.match_rule_alt({(0, (0,))}, test_line, self.rules_dict[0])
        solutions = {(test_line_index, applied_rules)
                     for test_line_index, applied_rules in possibilities
                     if test_line_index == len(test_line)}
        if with_print:
            print(f'{index} {test_line}: {solutions}')
        return len(solutions) > 0


def check(rules_dict, test_lines, with_print=False):
    grammar_checker = GrammarChecker(rules_dict)
    return sum(1 for index, test_line in enumerate(test_lines)
               if grammar_checker.match_rule_first(index, test_line, with_print=with_print))


def test_1st():
    assert check(*parse_input(TEST_INPUT, replace=False), with_print=True) == 2
    assert check(*parse_input(TEST_INPUT_2ND, replace=False), with_print=True) == 3


def test_2nd():
    rules_dict = parse_input(TEST_INPUT_2ND)[0]
    grammar_checker = GrammarChecker(rules_dict)
    assert not grammar_checker.match_rule_first(0, "a")
    assert grammar_checker.match_rule_first(0, "bbabbbbaabaabba")
    assert grammar_checker.match_rule_first(0, "babbbbaabbbbbabbbbbbaabaaabaaa")
    assert not grammar_checker.match_rule_first(0, "aaaabbaaaabbaaa")
    assert check(*parse_input(TEST_INPUT_2ND), with_print=True) == 12


def reddit_solution(my_input):
    inp_str = my_input.split('\n\n')
    rls = {exp[:exp.find(':')]: exp[exp.find(':') + 2:]
           for exp in inp_str[0].split('\n')}
    exps = inp_str[1].split('\n')

    # ugly but efficient (but no general solution)
    @lru_cache(137)
    def cmp(ind, dpth=0):
        curr = rls[ind]
        return ('' if dpth > 4
                else (curr[1]
                      if '"' in curr
                      else (f'''({"|".join([''.join([(cmp(i)
                                                      if i != ind
                                                      else f'({cmp(ind, dpth + 1)})')
                                                     for i in prt.split()])
                                            for prt in curr.split('|')])})'''
                            if '|' in curr
                            else (r''.join([cmp(i) for i in curr.split()])))))

    def first_part():
        return sum(re.fullmatch(cmp('0'), exp) is not None for exp in exps)

    def second_part():
        rls['8'], rls['11'] = '42 | 42 8', '42 31 | 42 11 31'
        return sum(re.fullmatch(cmp('0'), exp) is not None for exp in exps)

    print(first_part())
    cmp.cache_clear()
    print(second_part())


reddit_solution(PUZZLE_INPUT)

test_1st()
print(check(*parse_input(PUZZLE_INPUT, replace=False), with_print=True))

test_2nd()
print(check(*parse_input(PUZZLE_INPUT), with_print=True))
