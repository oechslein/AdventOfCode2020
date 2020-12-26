import collections
from typing import List

import numpy as np

from Utils import multiply, is_co_prime, is_prime
from input import TEST_INPUT, PUZZLE_INPUT, PUZZLE_INPUT_AHA, PUZZLE_INPUT_JAGGER

BusType = collections.namedtuple('bus_type', ['offset', 'interval'])


def parse_input(my_input):
    my_timestamp, busses = my_input.strip().split('\n')
    return int(my_timestamp), \
           [BusType(offset, int(bus)) for offset, bus in enumerate(busses.split(',')) if bus != 'x']


def slow_solution(my_input: List[BusType]):
    def fits_schedule(curr_timestamp: int, bus: BusType):
        return ((curr_timestamp + bus.offset) % bus.interval) == 0

    my_input.sort(key=lambda x: x.interval, reverse=True)
    slowest_bus = my_input[0]
    curr_timestamp = slowest_bus.interval - slowest_bus.offset
    interval = slowest_bus.interval
    assert fits_schedule(curr_timestamp, slowest_bus)

    second_slowest_bus = my_input[1]
    while not fits_schedule(curr_timestamp, second_slowest_bus):
        curr_timestamp += interval
    interval *= second_slowest_bus.interval

    while not all(fits_schedule(curr_timestamp, bus) for bus in my_input[2:]):
        curr_timestamp += interval
    return curr_timestamp


assert slow_solution(parse_input(TEST_INPUT)[1]) == 1068781


# print(slow_solution(parse_input(PUZZLE_INPUT)[1]))


def faster_solution(my_input: list):
    def fits_schedule(curr_timestamp: int, bus: BusType):
        return ((curr_timestamp + bus.offset) % bus.interval) == 0

    def get_next_timestamp(curr_timestamp: int, bus: BusType, interval: int):
        # find next timestamp based on the given interval that the bus interval/offset fits as well
        while not fits_schedule(curr_timestamp, bus):
            curr_timestamp += interval
        return curr_timestamp

    def calc_solution_rec(curr_timestamp: int, interval: int, remaining_input: List[BusType]):
        if not remaining_input:
            # remaining input is empty
            return curr_timestamp

        next_bus = remaining_input[0]

        # recursive call of remaining list (without first element),
        # new interval is old_interval * interval from bus
        #  (that is the next time all conditions of previous busses and new bus are met)
        return calc_solution_rec(curr_timestamp=get_next_timestamp(curr_timestamp, next_bus, interval),
                                 interval=np.lcm(interval, next_bus.interval, dtype=np.uint64),
                                 remaining_input=remaining_input[1:])

    # sort input with highest interval first
    my_input.sort(key=lambda bus: bus.interval, reverse=True)
    min_timestamp = calc_solution_rec(curr_timestamp=np.uint64(1), interval=np.uint64(1), remaining_input=my_input)

    assert all(fits_schedule(min_timestamp, bus) for bus in my_input)
    return min_timestamp


assert faster_solution(parse_input(TEST_INPUT)[1]) == 1068781
print('Jacky', faster_solution(parse_input(PUZZLE_INPUT)[1]))
print('Aha', faster_solution(parse_input(PUZZLE_INPUT_AHA)[1]))
print('Jagger', faster_solution(parse_input(PUZZLE_INPUT_JAGGER)[1]))


def check_co_primes(my_input: List[BusType]):
    first_bus = None
    for bus in my_input:
        assert is_prime(bus.interval), bus.interval
        if first_bus is not None:
            assert is_co_prime(first_bus.interval, bus.interval), (first_bus.interval, bus.interval)
        first_bus = bus


def cheat_solution(my_input):
    check_co_primes(my_input)
    interval = multiply(bus.interval for bus in my_input)
    result = 0
    for bus in my_input:
        p = interval // bus.interval
        result += -bus.offset * pow(p, -1, bus.interval) * p
    return result % interval


assert cheat_solution(parse_input(TEST_INPUT)[1]) == 1068781
print('Jacky', cheat_solution(parse_input(PUZZLE_INPUT)[1]))


def aha_solution(my_input: List[BusType], start_t=0):
    def fits_schedule(curr_timestamp: int, bus: BusType):
        return ((curr_timestamp + bus.offset) % bus.interval) == 0

    t = start_t

    while True:
        t_prev = t
        found = True
        for idt in my_input:
            dt = int((np.floor((np.double(t) - np.double(0.5)) / np.double(idt.interval)) + 1) * idt.interval - t)
            if dt != idt.offset:
                t += idt.interval + dt - idt.offset
                found = False
                break
        if found:
            min_timestamp = t
            break
        if t == t_prev:
            assert False

    assert all(fits_schedule(min_timestamp, bus) for bus in my_input)
    return min_timestamp


assert aha_solution(parse_input(TEST_INPUT)[1]) == 1068781
# print('AHA Solution mit AHA', aha_solution(parse_input(PUZZLE_INPUT_AHA)[1], start_t=1010182346200000))
# 1010182346291467
