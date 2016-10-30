import random


def random_pop(some_list):
    """Randomly remove an element from the given list and return the removed element.
    """
    index = random.randint(0, len(some_list) - 1)
    return some_list.pop(index)
