"""A bot to handle countdown games.

At the moment, it recognises only one pattern: '[01234] from the top'.

It could be extended by adding other patterns (e.g. 'inverted T' etc) that
then call `numbers_game` with the relevant number from the top.

This doesn't (yet) play any letters games or conundrums.
"""
import re

from copy import deepcopy

from slackbot.bot import Bot, listen_to

from countdown_slackbot import numbers


DEFAULT_STATE = ([], 0)
USER_STATES = {}


def get_user_state(user):
    user_id = user["id"]

    if user_id not in USER_STATES:
        USER_STATES[user_id] = deepcopy(DEFAULT_STATE)

    return USER_STATES[user_id]


def set_user_state(user, state):
    user_id = user["id"]
    USER_STATES[user_id] = state


@listen_to("^([01234]) from the top.*$", re.IGNORECASE)
def chat_message(message, str_num_from_top_row):
    try:
        num_from_top_row = int(str_num_from_top_row)
    except (ValueError, TypeError):
        message.reply("Need a number between 0-4 from the top row")
        return

    return numbers_game(message, num_from_top_row)


@listen_to("^([0-9]+ . [0-9]+ = [0-9]+)$")
def calculation(message, line):
    calculation = numbers.Calculation.parse(line)

    if not hasattr(message, "user"):
        print(type(message))
        print(message)
        return

    try:
        (current_numbers, target) = get_user_state(message.user)
    except KeyError:
        return

    try:
        calculation.apply(current_numbers)
    except numbers.InvalidAssertionError:
        response = "{} is *not* true".format(calculation)
        message.reply(response)
        return
    except numbers.BadCalculationError as e:
        message.reply(str(e))
        return

    if target in current_numbers:
        message.reply("Congrats!")
    else:
        message.reply("Yes: {}".format(calculation))

    set_user_state(message.user, (current_numbers, target))


@listen_to("^reset$", re.IGNORECASE)
def reset(message):
    set_user_state(message.user, DEFAULT_STATE)


def numbers_game(message, num_from_top_row):
    global DEFAULT_STATE

    try:
        numbers_as_ints = numbers.pick_numbers(num_from_top_row)
    except ValueError as e:
        message.reply("Couldn't pick numbers: {0}".format(e))
        return
    numbers_as_strings = map(str, numbers_as_ints)

    target = numbers.generate_target()
    DEFAULT_STATE = (numbers_as_ints, target)
    for user_id in list(USER_STATES):
        del USER_STATES[user_id]

    response = "Target is {0} from {1}".format(
        target, ", ".join(numbers_as_strings)
    )
    message.reply(response)


def main():
    bot = Bot()
    bot.run()
