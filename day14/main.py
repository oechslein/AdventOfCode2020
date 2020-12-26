import collections
import re
from typing import Union, List, Optional

import bitstring

from input import TEST_INPUT, PUZZLE_INPUT

MaskInputType = collections.namedtuple('MaskInputType', ['mask_0', 'mask_1'])
MemInputType = collections.namedtuple('MemInputType', ['mem_addr', 'mem_value'])


def parse_input(my_input_str: str) -> List[Union[MaskInputType, MemInputType]]:
    my_input_list = []
    for my_input_str in my_input_str.strip().split('\n'):
        if my_input_str.startswith('mask ='):
            mask_str = my_input_str.replace('mask = ', '')
            mask_0 = bitstring.BitArray(bin=mask_str.replace('1', 'X').replace('0', '1').replace('X', '0'))
            mask_1 = bitstring.BitArray(bin=mask_str.replace('0', 'X').replace('1', '1').replace('X', '0'))
            my_input_list.append(MaskInputType(mask_0, mask_1))
        else:
            result = re.fullmatch(r'mem\[(\d+)\] = (\d+)', my_input_str)
            mem_addr = int(result[1])
            bit_str = bin(int(result[2])).replace('0b', '')
            bit_str = ('0' * (36 - len(bit_str))) + bit_str
            assert len(bit_str) == 36
            mem_value = bitstring.BitArray(bin=bit_str)
            my_input_list.append(MemInputType(mem_addr, mem_value))
    return my_input_list


def overwrite(mem_value: bitstring.BitArray, mask: bitstring.BitArray, overwrite_value: bool):
    for index, value in enumerate(mask):
        if value:
            mem_value[index] = overwrite_value
    return mem_value


def modify(mem_value: bitstring.BitArray, mask: MaskInputType):
    mem_value = overwrite(mem_value, mask.mask_0, False)
    mem_value = overwrite(mem_value, mask.mask_1, True)
    return mem_value.uint


def calc(my_input_list: List[Union[MaskInputType, MemInputType]]):
    mem_dict = {}
    mask: Optional[MaskInputType] = None
    for my_input in my_input_list:
        if isinstance(my_input, MaskInputType):
            mask = my_input
        else:
            assert isinstance(my_input, MemInputType)
            mem_dict[my_input.mem_addr] = modify(my_input.mem_value, mask)
    return sum(mem_dict.values())


assert calc(parse_input(TEST_INPUT)) == (101 + 64)
print(calc(parse_input(PUZZLE_INPUT)))
