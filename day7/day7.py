import re

from day7_input import TEST_INPUT, PUZZLE_INPUT, TEST_INPUT_2


def parse_input(my_input):
    bag_dict = {}
    # light red bags contain 1 bright white bag, 2 muted yellow bags.
    bag_pattern = re.compile(r'(?P<color>.*) bags contain (?P<bag_content>.*)\.')
    bag_color_pattern = re.compile(r'(?P<bag_amount>\d+) (?P<color>[^,]*) bag,? ?')
    for bag_result in bag_pattern.finditer(my_input):
        bag_colors = {}
        for bag_color_result in bag_color_pattern.finditer(bag_result['bag_content']):
            bag_colors[bag_color_result['color']] = int(bag_color_result['bag_amount'])
        bag_dict[bag_result['color']] = bag_colors
    return bag_dict


def count_bags_that_contain(bag_dict, color_to_find):
    def can_bags_contain_rec(content):
        for inner_color, amount in content.items():
            if inner_color == color_to_find:
                return True
            else:
                if can_bags_contain_rec(bag_dict[inner_color]):
                    return True
        return False

    return sum(1 for content in bag_dict.values() if can_bags_contain_rec(content))


print(parse_input(TEST_INPUT))
MY_BAG_COLOR = 'shiny gold'
assert count_bags_that_contain(parse_input(TEST_INPUT), MY_BAG_COLOR) == 4, \
    count_bags_that_contain(parse_input(TEST_INPUT), MY_BAG_COLOR)
print(count_bags_that_contain(parse_input(PUZZLE_INPUT), MY_BAG_COLOR))


### 2nd

def count_bags(bag_dict, color_to_find):
    def count_bags_rec(curr_color_to_find):
        return 1 + sum(amount * count_bags_rec(inner_color)
                       for inner_color, amount in bag_dict[curr_color_to_find].items())

    return count_bags_rec(color_to_find) - 1


assert count_bags(parse_input(TEST_INPUT), MY_BAG_COLOR) == 32, count_bags(parse_input(TEST_INPUT), MY_BAG_COLOR)
assert count_bags(parse_input(TEST_INPUT_2), MY_BAG_COLOR) == 126, count_bags(parse_input(TEST_INPUT_2), MY_BAG_COLOR)

print(count_bags(parse_input(PUZZLE_INPUT), MY_BAG_COLOR))
