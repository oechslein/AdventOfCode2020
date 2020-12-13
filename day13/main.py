import collections
import time

import numpy as np

import re
from Utils import multiply
from input import TEST_INPUT, PUZZLE_INPUT

def get_prime_numbers_until(max_int=59):
    primes = list(range(2, max_int+1))
    for index in range(len(primes)):
        if primes[index] is not None:
            for index_2 in range(index+primes[index], len(primes), primes[index]):
                primes[index_2] = None
    return [prime for prime in primes if prime]

print(get_prime_numbers_until())
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
# 7,13,x,x,59,x,31,19

def parse_input(my_input):
    timestamp, buslines = my_input.strip().split('\n')
    return int(timestamp), list(sorted(int(busline) for busline in buslines.split(',') if busline != 'x'))

def get_earliest_busline(timestamp, buslines):
    buslines_dict = {busline: ((timestamp // busline) + 1) * busline for busline in buslines}
    min_busline, min_timestamp_busline = min(buslines_dict.items(), key=lambda timestamp_busline_tuple: timestamp_busline_tuple[1])
    return (min_timestamp_busline - timestamp) * min_busline

assert get_earliest_busline(*parse_input(TEST_INPUT)) == ((944 - 939) * 59)

print(get_earliest_busline(*parse_input(PUZZLE_INPUT)))
