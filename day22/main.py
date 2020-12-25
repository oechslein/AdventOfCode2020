import collections
import functools
import itertools
import operator
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, List, Optional

import numpy as np

from Utils import multiply, count
from input import PUZZLE_INPUT

import sys

import re


TEST_INPUT = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

@dataclass
class Player(object):
    number: int
    deck: List[int]

    @classmethod
    def parse_player(cls, player_string: str) -> "Player":
        my_list = player_string.strip().split('\n')
        number = int(re.fullmatch(r'Player (\d+):', my_list[0])[1])
        start_deck = list(map(int, my_list[1:]))
        return Player(number, start_deck)

    def draw_top_card(self) -> int:
        return self.deck.pop(0)

    def give_cards(self, cards: List[int]):
        self.deck += cards

    def deck_score(self):
        return sum((index+1)*value for index, value in enumerate(reversed(self.deck)))


def parse_input(my_input: str):
    return list(map(Player.parse_player, my_input.strip().split('\n\n')))


def play_round(*players: Player):
    highest_card = -1
    top_player: Optional[Player] = None
    all_cards = []
    for player in players:
        top_card = player.draw_top_card()
        if top_card > highest_card:
            highest_card = top_card
            top_player = player
        all_cards.append(top_card)
    assert top_player
    top_player.give_cards(sorted(all_cards, reverse=True))
    return top_player


def play_rounds(*players: Player, with_output=False):
    i = 1
    top_player = None
    while all(len(player.deck) > 0 for player in players):
        if with_output:
            print(f'-- Round {i} --')
        if with_output:
            for player in players:
                print(f"-- Player {player.number}'s deck: {','.join(map(str, player.deck))} --")
        top_player = play_round(*players)
        if with_output:
            print(f'-- Player {top_player.number} wins the round! --')
        i += 1
    assert top_player
    return top_player.deck_score()


assert play_rounds(*parse_input(TEST_INPUT)) == 306

print(play_rounds(*parse_input(PUZZLE_INPUT)))

