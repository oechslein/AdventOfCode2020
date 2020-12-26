import cProfile
import time
from dataclasses import dataclass
from typing import Dict

from input import PUZZLE_INPUT


@dataclass(init=False)
class CupCircle(object):
    cups: Dict[int, int]
    current_cup: int

    def __init__(self, cup_string: str):
        input_circle = list(map(int, cup_string))
        self.cups = {input_circle[i]: input_circle[i + 1] for i in range(len(input_circle) - 1)}
        self.cups[input_circle[-1]] = input_circle[0]
        self.current_cup = input_circle[0]
        self.highest_cup = max(self.cups)
        self.lowest_cup = min(self.cups)

    def pick_up_cups(self):
        picked_up_cup_1 = self.cups[self.current_cup]
        picked_up_cup_2 = self.cups[picked_up_cup_1]
        picked_up_cup_3 = self.cups[picked_up_cup_2]
        self.cups[self.current_cup] = self.cups[picked_up_cup_3]
        return picked_up_cup_1, picked_up_cup_2, picked_up_cup_3

    def destination_cup_index(self, picked_up_cup_1, picked_up_cup_2, picked_up_cup_3):
        def wrap_around_if_needed(destination_cup):
            if destination_cup < self.lowest_cup:
                return self.highest_cup
            return destination_cup

        current_cup = self.current_cup
        destination_cup = wrap_around_if_needed(current_cup - 1)
        while destination_cup in (picked_up_cup_1, picked_up_cup_2, picked_up_cup_3):
            destination_cup = wrap_around_if_needed(destination_cup - 1)
        return destination_cup

    def place_cups(self, destination_cup: int, picked_up_cup_1, picked_up_cup_2, picked_up_cup_3):
        self.cups[destination_cup], self.cups[picked_up_cup_3] = picked_up_cup_1, self.cups[destination_cup]

    def get_cup_line(self):
        result = [f'({self.current_cup})']
        curr = self.cups[self.current_cup]
        while curr != self.current_cup:
            result.append(str(curr))
            curr = self.cups[curr]

        return f'cups: {" ".join(result)}'

    def play_round(self, with_print=False):
        if with_print:
            print(self.get_cup_line())
        picked_up_cup_1, picked_up_cup_2, picked_up_cup_3 = self.pick_up_cups()
        destination_cup = self.destination_cup_index(picked_up_cup_1, picked_up_cup_2, picked_up_cup_3)
        self.place_cups(destination_cup, picked_up_cup_1, picked_up_cup_2, picked_up_cup_3)
        if with_print:
            print(f'pick up: {", ".join(map(str, (picked_up_cup_1, picked_up_cup_2, picked_up_cup_3)))}')
            print(f'destination: {destination_cup}')
        self.current_cup = self.cups[self.current_cup]

    def play_rounds(self, amount=100, with_print=False) -> str:
        for i in range(amount):
            if with_print:
                print(f'-- move {i + 1} --')
            self.play_round(with_print=with_print)
            if with_print:
                print('')
        if with_print:
            print('-- final --')
            print(self.get_cup_line())

        cup_one_index = 1
        result = []
        curr = self.cups[cup_one_index]
        while curr != cup_one_index:
            result.append(curr)
            curr = self.cups[curr]
        return ''.join(map(str, result))


TEST_INPUT = "389125467"

assert CupCircle(TEST_INPUT).play_rounds(10, with_print=True) == '92658374'
assert CupCircle(TEST_INPUT).play_rounds(100, with_print=True) == '67384529'

print(CupCircle(PUZZLE_INPUT).play_rounds(amount=100, with_print=False))

start_time = time.time()
amount = 100000
CupCircle(PUZZLE_INPUT).play_rounds(amount=amount, with_print=False)
print(f'Duration: {time.time() - start_time}, {(time.time() - start_time) / amount} per round')

pr = cProfile.Profile()
pr.enable()
CupCircle(PUZZLE_INPUT).play_rounds(amount=amount, with_print=False)
pr.disable()
# after your program ends
pr.print_stats(sort="calls")

# Amount: 100000
# Duration: 0.5906565189361572, 5.906565189361572e-06 per round
# Cup => int nicht schneller
# no complete new list in pick_up (only in edge case)
# Duration: 0.4687497615814209, 4.687497615814209e-06 per round
# no assert
# Duration: 0.37778306007385254, 3.7778306007385256e-06 per round
