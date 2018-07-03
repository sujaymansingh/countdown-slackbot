import random

from copy import deepcopy
from operator import (add, sub, mul, floordiv)

from attr import attrs, attrib


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


class Operator():
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return "Operator('{}')".format(self.symbol)

    def __call__(self, *args, **kwargs):
        functions = {
            "+": add,
            "-": sub,
            "/": floordiv,
            "*": mul,
        }
        func = functions[self.symbol]
        return func(*args, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Operator) and other.symbol == self.symbol


PLUS = Operator("+")
SUBTRACT = Operator("-")
MULTIPLY = Operator("*")
DIVIDE = Operator("/")


@attrs(str=False)
class Calculation():

    num_1 = attrib()
    operator = attrib()
    num_2 = attrib()
    asserted_result = attrib()

    def __str__(self):
        return "{} {} {} = {}".format(
            self.num_1,
            self.operator.symbol,
            self.num_2,
            self.asserted_result,
        )

    @classmethod
    def parse(cls, line):
        """
        >>> Calculation.parse('3 + 9 = 12')
        Calculation(num_1=3, operator=Operator('+'), num_2=9, asserted_result=12)
        """
        parts = [part.strip() for part in line.strip().split(" ")]

        if len(parts) not in [5]:
            raise BadLineError("Must be 5 parts in {}".format(line))

        try:
            num_1 = int(parts[0])
            num_2 = int(parts[2])
            asserted_result = int(parts[4])
        except (ValueError, TypeError) as e:
            raise BadLineError(e)

        operator = Operator(parts[1])

        return Calculation(num_1=num_1, num_2=num_2, operator=operator, asserted_result=asserted_result)

    def apply(self, original_numbers):
        numbers = deepcopy(original_numbers)

        try:
            numbers.remove(self.num_1)
            numbers.remove(self.num_2)
        except ValueError:
            raise NumberNotPresentError("no number")

        actual_result = self.operator(self.num_1, self.num_2)

        if actual_result != self.asserted_result:
            raise InvalidAssertionError()

        # Everything was ok! Now we can make the modifications to the actual numbers
        original_numbers.remove(self.num_1)
        original_numbers.remove(self.num_2)
        original_numbers.append(self.asserted_result)


class BadLineError(Exception):
    pass


class BadCalculationError(Exception):
    pass


class NumberNotPresentError(BadCalculationError):
    pass


class InvalidAssertionError(BadCalculationError):
    pass
