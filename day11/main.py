import numpy as np

from Utils import count
from input import TEST_INPUT, PUZZLE_INPUT


def parse_input(my_input):
    return np.array([list(line) for line in my_input.strip().split('\n')])


def adjacent_seats(seats: np.ndarray, x: int, y: int):
    for new_x in (x - 1, x, x + 1):
        if 0 <= new_x < seats.shape[0]:
            for new_y in (y - 1, y, y + 1):
                if (new_x, new_y) != (x, y) and 0 <= new_x < seats.shape[0] and 0 <= new_y < seats.shape[1]:
                    yield seats[new_x, new_y]


def fulfills_empty(seats: np.ndarray, x: int, y: int):
    return all(seat in ('.', 'L') for seat in adjacent_seats(seats, x, y))


def fulfills_occupied(seats: np.ndarray, x: int, y: int):
    return count(seat for seat in adjacent_seats(seats, x, y) if seat in ('#',)) >= 4


def count_occupied(seats: np.ndarray):
    return count(seat for seat in seats.flatten() if seat == '#')


def stable_seat_count(seats: np.ndarray):
    while True:
        new_seats = seats.copy()
        for x in range(seats.shape[0]):
            for y in range(seats.shape[1]):
                if seats[x, y] == '.':
                    # ignore floor
                    pass
                elif seats[x, y] == 'L':
                    # empty seat check if it will be occupied
                    if fulfills_empty(seats, x, y):
                        new_seats[x, y] = '#'
                elif seats[x, y] == '#':
                    # occupied seat check if it will be empty
                    if fulfills_occupied(seats, x, y):
                        new_seats[x, y] = 'L'
        if np.array_equal(seats, new_seats):
            return count_occupied(seats)
        seats = new_seats


assert stable_seat_count(parse_input((TEST_INPUT))) == 37


# print(stable_seat_count(parse_input((PUZZLE_INPUT))))


# 2nd


def visible_seats(seats: np.ndarray, x: int, y: int):
    for direction_x in (-1, 0, 1):
        for direction_y in (-1, 0, 1):
            if (direction_x, direction_y) != (0, 0):
                visible_seat = None
                for i in range(1, max(seats.shape[0], seats.shape[1])):
                    new_x = x + direction_x * i
                    new_y = y + direction_y * i
                    if not (0 <= new_x < seats.shape[0] and 0 <= new_y < seats.shape[1]):
                        break
                    elif seats[new_x, new_y] == 'L':
                        visible_seat = 'L'
                        break
                    elif seats[new_x, new_y] == '#':
                        visible_seat = '#'
                        break
                if visible_seat is not None:
                    yield visible_seat


def fulfills_empty_2nd(seats: np.ndarray, x: int, y: int):
    return all(seat in ('.', 'L') for seat in visible_seats(seats, x, y))


def fulfills_occupied_2nd(seats: np.ndarray, x: int, y: int):
    return count(seat for seat in visible_seats(seats, x, y) if seat in ('#',)) >= 5


def stable_seat_count_2nd(seats: np.ndarray):
    while True:
        new_seats = seats.copy()
        for x in range(seats.shape[0]):
            for y in range(seats.shape[1]):
                if seats[x, y] == '.':
                    # ignore floor
                    pass
                elif seats[x, y] == 'L':
                    # empty seat check if it will be occupied
                    if fulfills_empty_2nd(seats, x, y):
                        new_seats[x, y] = '#'
                elif seats[x, y] == '#':
                    # occupied seat check if it will be empty
                    if fulfills_occupied_2nd(seats, x, y):
                        new_seats[x, y] = 'L'
        if np.array_equal(seats, new_seats):
            return count_occupied(seats)
        seats = new_seats


assert stable_seat_count_2nd(parse_input((TEST_INPUT))) == 26

print(stable_seat_count_2nd(parse_input((PUZZLE_INPUT))))
