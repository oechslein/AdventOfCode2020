import re
from dataclasses import dataclass, field
from typing import Tuple, List, Set

from input import PUZZLE_INPUT

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
    all_previous_decks: Set[Tuple[int]] = field(default_factory=set)

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
        return sum((index + 1) * value for index, value in enumerate(reversed(self.deck)))

    def remember_deck(self):
        self.all_previous_decks.add(tuple(self.deck))

    def had_same_deck_before(self):
        return tuple(self.deck) in self.all_previous_decks

    def reset_all_previous_decks(self):
        self.all_previous_decks.clear()


def parse_input(my_input: str):
    return list(map(Player.parse_player, my_input.strip().split('\n\n')))


def play_round(player1: Player, player2: Player, game: int, with_output=False):
    if player1.had_same_deck_before() and player2.had_same_deck_before():
        player2.deck = []  # instant win
        return player1

    player1.remember_deck()
    player2.remember_deck()

    top_card_player1 = player1.draw_top_card()
    top_card_player2 = player2.draw_top_card()

    if (top_card_player1 <= len(player1.deck)) \
            and (top_card_player2 <= len(player2.deck)):
        if with_output:
            print('Playing a sub-game to determine the winner...\n')
        player1_new = Player(player1.number, player1.deck[:top_card_player1].copy())
        player2_new = Player(player2.number, player2.deck[:top_card_player2].copy())
        sub_top_player = play_rounds(player1_new, player2_new, game=game + 1, with_output=with_output)
        if sub_top_player.number == player1.number:
            top_player = player1
            player1.give_cards([top_card_player1, top_card_player2])
        else:
            assert sub_top_player.number == player2.number
            top_player = player2
            player2.give_cards([top_card_player2, top_card_player1])
        if with_output:
            print(f'The winner of game {game + 1} is player {top_player.number}!\n')
            print(f'...anyway, back to game {game}')
    else:
        if top_card_player1 > top_card_player2:
            top_player = player1
            player1.give_cards(sorted([top_card_player1, top_card_player2], reverse=True))
        elif top_card_player2 > top_card_player1:
            top_player = player2
            player2.give_cards(sorted([top_card_player2, top_card_player1], reverse=True))
        else:
            assert False

    return top_player


def play_rounds(player1: Player, player2: Player, game: int = 1, with_output=False):
    if with_output:
        print(f'=== Game {game} ===')
    round = 1
    top_player = None
    while all(len(player.deck) > 0 for player in (player1, player2)):
        if with_output:
            print(f'\n-- Round {round} (Game {game}) --')
        if with_output:
            for player in (player1, player2):
                print(f"-- Player {player.number}'s deck: {','.join(map(str, player.deck))} --")
        top_player = play_round(player1, player2, game=game, with_output=with_output)
        if with_output:
            print(f'-- Player {top_player.number} wins round {round} of game {game}! --')
        round += 1
        # player1.reset_all_previous_decks()
        # player2.reset_all_previous_decks()
    assert top_player

    if game == 1:
        print(f'\n\n== Post-game results ==\n'
              f"Player 1's deck: {','.join(map(str, player1.deck))}\n"
              f"Player 2's deck: {','.join(map(str, player2.deck))}\n")

    return top_player


assert play_rounds(*parse_input(TEST_INPUT), with_output=True).deck_score() == 291

print(play_rounds(*parse_input(PUZZLE_INPUT)).deck_score())
