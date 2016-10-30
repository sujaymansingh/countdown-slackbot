import random


def random_pop(some_list):
    """Randomly remove an element from the given list and return the removed element.
    """
    index = random.randint(0, len(some_list) - 1)
    return some_list.pop(index)


def pick_numbers(num_from_top_row, total_num_required=6):
    """Pick 6 random numbers, with 0-4 of them being from the top row.
    """
    # Ensure we have an int
    if not isinstance(num_from_top_row, int):
        raise ValueError(
            "num_from_top_row must be an int, instead got '{0}'".format(num_from_top_row)
        )

    top_row, bottom_row = get_basic_number_rows()

    if num_from_top_row < 0 or num_from_top_row > len(top_row):
        raise ValueError(
            "num_from_top_row must be between 0 and {0}".format(len(top_row))
        )

    if total_num_required - num_from_top_row > len(bottom_row):
        raise ValueError("Not enough numbers to satisfy total_num_required")

    numbers = []

    for i in range(num_from_top_row):
        numbers.append(random_pop(top_row))

    while len(numbers) < total_num_required:
        numbers.append(random_pop(bottom_row))

    return numbers


def get_basic_number_rows():
    """Returns two lists, one of the 'top' row and one of the 'bottom' row of numbers.

    'The tiles are arranged into two groups: four "large numbers" (25, 50, 75 and 100)
    (12, 37, 62, 87 in some special episodes) and the remainder "small numbers",
    which comprise two each of the numbers 1 to 10.'
    https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_round
    """
    top_row = [25, 50, 75, 100]
    bottom_row = []
    for i in range(1, 11):
        bottom_row.append(i)
        bottom_row.append(i)
    return top_row, bottom_row


def generate_target(min=100, max=999):
    return random.randint(100, 999)
