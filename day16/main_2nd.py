import re
from dataclasses import dataclass
from typing import List, Set, Tuple, Dict

from Utils import multiply
from input import PUZZLE_INPUT, TEST_INPUT


@dataclass(frozen=True)
class Rule(object):
    name: str
    start1: int
    end1: int
    start2: int
    end2: int

    def check_number(self, x):
        return self.start1 <= x <= self.end1 or self.start2 <= x <= self.end2


def parse_input(my_input_str: str):
    classes_str, my_ticket_str, nearby_tickets_str = my_input_str.strip().split('\n\n')
    rules = {((result := re.fullmatch(r'([^:]+): (\d+)-(\d+) or (\d+)-(\d+)', class_str))
              and Rule(result.group(1), int(result.group(2)), int(result.group(3)), int(result.group(4)), int(result.group(5))))
             for class_str in classes_str.split('\n')}
    my_ticket = list(map(int, my_ticket_str.replace('your ticket:\n', '').split(',')))
    nearby_tickets = [tuple(map(int, nearby_ticket_str.split(',')))
                      for nearby_ticket_str in nearby_tickets_str.replace('nearby tickets:\n', '').split('\n')]
    return rules, my_ticket, nearby_tickets


MULTIPLE_RESULT = False


def get_invalid_tickets(rules: Set[Rule], my_ticket: Tuple[int], nearby_tickets: List[Tuple[int]]):
    def get_invalid_ticket_numbers(curr_rules: Set[Rule], remaining_curr_ticket: Tuple[int]):
        if not remaining_curr_ticket:
            return []

        curr_ticket_number = remaining_curr_ticket[0]
        all_valid_rules = [rule for rule in rules if rule.check_number(curr_ticket_number)]
        if not all_valid_rules:
            return [curr_ticket_number]

        # now we have to mark/remove used rule
        # if more than one rule we have to backtrack or just calc for all found rules if
        result = []
        for used_rule in all_valid_rules:
            result = get_invalid_ticket_numbers(curr_rules - {used_rule}, remaining_curr_ticket[1:])
            if not result:
                return []
            elif not MULTIPLE_RESULT:
                return result
        return result

    def get_invalid_tickets_rec(curr_rules: Set[Rule], remaining_nearby_tickets: List[Tuple[int]]):
        if not remaining_nearby_tickets:
            return set()

        invalid_tickets = get_invalid_tickets_rec(curr_rules, remaining_nearby_tickets[1:])

        curr_ticket = remaining_nearby_tickets[0]
        invalid_ticket_numbers = get_invalid_ticket_numbers(curr_rules, curr_ticket)
        if invalid_ticket_numbers:
            invalid_tickets.add(curr_ticket)
        return invalid_tickets

    return get_invalid_tickets_rec(rules, nearby_tickets)


def get_valid_tickets(rules: Set[Rule], my_ticket: Tuple[int], nearby_tickets: List[Tuple[int]]):
    return set(nearby_tickets) - get_invalid_tickets(rules, my_ticket, nearby_tickets)


def calc_field_mapping(rules: Set[Rule], my_ticket: Tuple[int], nearby_tickets: List[Tuple[int]]):
    rule_index_mapping: Dict[Rule, Set[int]] = {rule: set(range(len(my_ticket))) for rule in rules}
    for rule, index_set in rule_index_mapping.items():
        assert len(index_set) > 0, rule_index_mapping

    valid_tickets = get_valid_tickets(rules, my_ticket, nearby_tickets)
    for valid_ticket in valid_tickets:
        for index, valid_ticket_number in enumerate(valid_ticket):
            for rule in rules:
                if not rule.check_number(valid_ticket_number):
                    rule_index_mapping[rule].discard(index)
                    assert len(rule_index_mapping[rule]) > 0

    for rule in sorted(rules, key=lambda rule: len(rule_index_mapping[rule])):
        for curr_rule in rules:
            if curr_rule != rule:
                rule_index_mapping[curr_rule].difference_update(rule_index_mapping[rule])

    for rule, index_set in rule_index_mapping.items():
        assert len(index_set) == 1, rule_index_mapping
    return {rule: index_set.pop() for rule, index_set in rule_index_mapping.items()}


def get_result(rules: Set[Rule], my_ticket: Tuple[int], nearby_tickets: List[Tuple[int]]):
    departure_rules = [rule for rule in rules if rule.name.startswith('departure')]
    field_mappping = calc_field_mapping(rules, my_ticket, nearby_tickets)
    return multiply(my_ticket[field_mappping[departure_rule]] for departure_rule in departure_rules)


assert get_invalid_tickets(*parse_input(TEST_INPUT)) == {(55, 2, 20), (40, 4, 50), (38, 6, 12)}, \
    get_invalid_tickets(*parse_input(TEST_INPUT))
assert get_valid_tickets(*parse_input(TEST_INPUT)) == {(7, 3, 47)}, \
    get_valid_tickets(*parse_input(TEST_INPUT))
# print(get_valid_tickets(*parse_input(TEST_INPUT_2ND)))
# print(calc_field_mapping(*parse_input(TEST_INPUT_2ND)))

print(get_result(*parse_input(PUZZLE_INPUT)))
