import re
import time
from dataclasses import dataclass
from typing import List, Set

from input import TEST_INPUT, PUZZLE_INPUT


@dataclass(frozen=True)
class Rule(object):
    interval1_start: int
    interval1_end: int
    interval2_start: int
    interval2_end: int

    def check_number(self, x):
        return self.interval1_start <= x <= self.interval1_end or self.interval2_start <= x <= self.interval2_end


def parse_input(my_input_str: str):
    classes_str, my_ticket_str, nearby_tickets_str = my_input_str.strip().split('\n\n')
    rules = {((result := re.fullmatch(r'([^:]+): (\d+)-(\d+) or (\d+)-(\d+)', class_str))
              and Rule(int(result.group(2)), int(result.group(3)), int(result.group(4)), int(result.group(5))))
             for class_str in classes_str.split('\n')}
    my_ticket = list(map(int, my_ticket_str.replace('your ticket:\n', '').split(',')))
    nearby_tickets = [list(map(int, nearby_ticket_str.split(',')))
                      for nearby_ticket_str in nearby_tickets_str.replace('nearby tickets:\n', '').split('\n')]
    return rules, my_ticket, nearby_tickets

MULTIPLE_RESULT = False

def get_invalid_ticket_numbers(rules: Set[Rule], my_ticket, nearby_tickets: List[List[int]]):
    del my_ticket

    def get_invalid_ticket_numbers(curr_rules: Set[Rule], curr_ticket):
        if not curr_ticket:
            return []

        curr_ticket_number = curr_ticket[0]
        all_valid_rules = [rule for rule in rules if rule.check_number(curr_ticket_number)]
        if not all_valid_rules:
            return [curr_ticket_number]

        # now we have to mark/remove used rule
        # if more than one rule we have to backtrack or just calc for all found rules if
        result = []
        for used_rule in all_valid_rules:
            result = get_invalid_ticket_numbers(curr_rules - {used_rule}, curr_ticket[1:])
            if not result:
                return []
            elif not MULTIPLE_RESULT:
                return result
        return result

    def get_invalid_ticket_numbers_rec(curr_rules: Set[Rule], remaining_nearby_tickets: List[List[int]]):
        print('remaining_nearby_tickets', len(remaining_nearby_tickets), time.time())
        if not remaining_nearby_tickets:
            return []

        nearby_ticket = remaining_nearby_tickets[0]
        invalid_ticket_numbers = get_invalid_ticket_numbers(curr_rules, nearby_ticket)
        return invalid_ticket_numbers + get_invalid_ticket_numbers_rec(curr_rules, remaining_nearby_tickets[1:])

    return get_invalid_ticket_numbers_rec(rules, nearby_tickets)


print(get_invalid_ticket_numbers(*parse_input(TEST_INPUT)))
assert sum(get_invalid_ticket_numbers(*parse_input(TEST_INPUT))) == (4 + 55 + 12)
print(sum(get_invalid_ticket_numbers(*parse_input(PUZZLE_INPUT))))
