import collections
import functools
import itertools
import operator
from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, List

import numpy as np

from Utils import multiply, count
from input import PUZZLE_INPUT, TEST_INPUT

import sys

import re


class Ingredient(str):
    pass


class Allergen(str):
    pass


@dataclass(frozen=True)
class Food(object):
    ingredients: Tuple[Ingredient]
    known_allergens: Tuple[Allergen]


"""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""


def parse_input(my_input: str):
    def parse_food(line):
        result = re.fullmatch(r'(.*) \(contains (.*)\)', line)
        return Food(tuple(Ingredient(ingredient) for ingredient in result[1].split(' ')),
                    tuple(Allergen(allergen) for allergen in result[2].split(', ')))

    return tuple(parse_food(line) for line in my_input.strip().split('\n'))


def calc1st(food_list: Tuple[Food]):
    all_ingredients = set(ingredient for food in food_list for ingredient in food.ingredients)
    all_allergens = set(allergen for food in food_list for allergen in food.known_allergens)
    allergen_possible_ingredient_map = {}
    for food in food_list:
        for allergen in food.known_allergens:
            if allergen not in allergen_possible_ingredient_map:
                allergen_possible_ingredient_map[allergen] = set(food.ingredients)
            else:
                allergen_possible_ingredient_map[allergen].intersection_update(food.ingredients)

    allergen_ingredients = {allergen for allergen_set in allergen_possible_ingredient_map.values()
                            for allergen in allergen_set}
    no_allergen_ingredients = {ingredient for ingredient in all_ingredients
                               if ingredient not in allergen_ingredients}

    no_allergen_ingredients_appear_count = sum(no_allergen_ingredient in food.ingredients
                                               for no_allergen_ingredient in no_allergen_ingredients
                                               for food in food_list)

    return no_allergen_ingredients_appear_count


assert calc1st(parse_input(TEST_INPUT)) == 5
print(calc1st(parse_input(PUZZLE_INPUT)))


def calc2nd(food_list: Tuple[Food]):
    all_ingredients = set(ingredient for food in food_list for ingredient in food.ingredients)
    all_allergens = set(allergen for food in food_list for allergen in food.known_allergens)
    allergen_possible_ingredient_map = {}
    for food in food_list:
        for allergen in food.known_allergens:
            if allergen not in allergen_possible_ingredient_map:
                allergen_possible_ingredient_map[allergen] = set(food.ingredients)
            else:
                allergen_possible_ingredient_map[allergen].intersection_update(food.ingredients)

    allergen_ingredients = {allergen for allergen_set in allergen_possible_ingredient_map.values()
                            for allergen in allergen_set}
    no_allergen_ingredients = {ingredient for ingredient in all_ingredients
                               if ingredient not in allergen_ingredients}

    no_allergen_ingredients_appear_count = sum(no_allergen_ingredient in food.ingredients
                                               for no_allergen_ingredient in no_allergen_ingredients
                                               for food in food_list)

    found = True
    while found:
        found = False
        for allergen, possible_ingredients in allergen_possible_ingredient_map.items():
            if len(possible_ingredients) == 1:
                fixed_ingredient = list(possible_ingredients)[0]
                for other_allergen, other_possible_ingredients in allergen_possible_ingredient_map.items():
                    if other_allergen != allergen and fixed_ingredient in other_possible_ingredients:
                        other_possible_ingredients.remove(fixed_ingredient)
                        found = True

    ingredient_allergen_map = {list(possible_ingredients)[0]: allergen
                               for allergen, possible_ingredients in allergen_possible_ingredient_map.items()}

    return ','.join(sorted(ingredient_allergen_map,
                           key=lambda ingredient: ingredient_allergen_map[ingredient]))


assert calc2nd(parse_input(TEST_INPUT)) == 'mxmxvkd,sqjhc,fvjkl'
print(calc2nd(parse_input(PUZZLE_INPUT)))
