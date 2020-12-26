import collections
import re
from typing import Union, List, Optional

import bitstring

from input import PUZZLE_INPUT, TEST_INPUT_2

MaskInputType = collections.namedtuple('MaskInputType', ['mask_0', 'mask_1', 'mask_X'])
MemInputType = collections.namedtuple('MemInputType', ['mem_addr', 'mem_value'])


def get_bitsstring(value, but_length=36):
    bit_str = bin(int(value)).replace('0b', '')
    bit_str = ('0' * (but_length - len(bit_str))) + bit_str
    assert len(bit_str) == but_length
    return bitstring.BitArray(bin=bit_str)


def parse_input(my_input_str: str) -> List[Union[MaskInputType, MemInputType]]:
    my_input_list = []
    for my_input_str in my_input_str.strip().split('\n'):
        if my_input_str.startswith('mask ='):
            mask_str = my_input_str.replace('mask = ', '')
            mask_0 = bitstring.BitArray(bin=mask_str.replace('1', 'X').replace('0', '1').replace('X', '0'))
            mask_1 = bitstring.BitArray(bin=mask_str.replace('0', 'X').replace('1', '1').replace('X', '0'))
            mask_X = bitstring.BitArray(bin=mask_str.replace('0', '0').replace('1', '0').replace('X', '1'))
            my_input_list.append(MaskInputType(mask_0, mask_1, mask_X))
        else:
            result = re.fullmatch(r'mem\[(\d+)\] = (\d+)', my_input_str)
            mem_addr = get_bitsstring(result[1])
            mem_value = int(result[2])
            my_input_list.append(MemInputType(mem_addr, mem_value))
    return my_input_list


def floatable(mem_addr: bitstring.BitArray, mask: bitstring.BitArray):
    amount_of_trues = mask.count(True)
    for possible_setting in range(2 ** amount_of_trues):
        possible_setting = get_bitsstring(possible_setting)
        possible_setting_index = -1
        for index in mask.findall([1]):
            mem_addr[index] = possible_setting[possible_setting_index]
            possible_setting_index -= 1
        yield mem_addr


def modify(mem_addr: bitstring.BitArray, mask: MaskInputType):
    mem_addr = ((mem_addr ^ mask.mask_1) | mem_addr)
    return floatable(mem_addr, mask.mask_X)


def calc(my_input_list: List[Union[MaskInputType, MemInputType]]):
    mem_dict = {}
    mask: Optional[MaskInputType] = None
    for index, my_input in enumerate(my_input_list):
        if isinstance(my_input, MaskInputType):
            mask = my_input
        else:
            assert isinstance(my_input, MemInputType)
            for mem_addr in modify(my_input.mem_addr, mask):
                mem_dict[mem_addr.uint] = my_input.mem_value
    return sum(mem_dict.values())


assert calc(parse_input(TEST_INPUT_2)) == 208
print(calc(parse_input(PUZZLE_INPUT)))
