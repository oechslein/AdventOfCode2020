import collections
import operator
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple

import numpy as np

from input import PUZZLE_INPUT, TEST_INPUT

import sys
import pyparsing

ppc = pyparsing.pyparsing_common

pyparsing.ParserElement.enablePackrat()
sys.setrecursionlimit(3000)


arithOp = pyparsing.oneOf("+ - * / ^")

expr = pyparsing.infixNotation(
    ppc.integer,
    [
        (arithOp, 2, pyparsing.opAssoc.LEFT),
    ],
)

opn = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}

def parse_input(my_input):
    return [expr.parseString(line)[0] for line in my_input.strip().split('\n')]


def calc(parse_result):
    if isinstance(parse_result, Number):
        return parse_result
    elif isinstance(parse_result, str):
        return opn[parse_result]
    else:
        value1, op, value2 = map(calc, parse_result[0:3])
        result = op(value1, value2)
        if parse_result[3:]:
            return calc([result] + parse_result[3:])
        else:
            return result

def calc_list(parse_result_list):
    return sum(calc(parse_result) for parse_result in parse_result_list)


assert calc_list(parse_input(TEST_INPUT)) == (26 + 437 + 12240 + 13632)
print(calc_list(parse_input(PUZZLE_INPUT)))
