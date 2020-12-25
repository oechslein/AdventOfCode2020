import abc
import cProfile
import collections
import functools
import itertools
import operator
import time
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, List, Optional, ClassVar, Set

import numpy as np

from Utils import multiply, count
from input import PUZZLE_INPUT

import sys

import re


def transform(subject_number: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


# 5764801 and 17807724 are public keys
public_key_card, public_key_door = 5764801, 17807724

assert transform(7, 8) == public_key_card
assert transform(7, 11) == public_key_door

encryption_key = 14897079
assert transform(public_key_door, 8) == encryption_key
assert transform(public_key_card, 11) == encryption_key

def calc_loop_sizes(subject_number: int):
    value = 1
    loop_size = 1
    while True:
        value *= subject_number
        value %= 20201227
        yield loop_size, value
        loop_size += 1

def find_loop_sizes(subject_number: int, *values_to_find: int):
    loop_sized = []
    for loop_size, value in calc_loop_sizes(subject_number):
        if value in values_to_find:
            loop_sized.append(loop_size)
            if len(loop_sized) == len(values_to_find):
                return loop_sized


public_key_card, public_key_door = 1614360, 7734663

loop_size_card, loop_size_door = find_loop_sizes(7, public_key_card, public_key_door)

print(transform(public_key_door, loop_size_card))
print(transform(public_key_card, loop_size_door))
