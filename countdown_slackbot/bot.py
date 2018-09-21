"""A bot to handle countdown games.

At the moment, it recognises only one pattern: '[01234] from the top'.

It could be extended by adding other patterns (e.g. 'inverted T' etc) that
then call `numbers_game` with the relevant number from the top.

This doesn't (yet) play any letters games or conundrums.
"""
import re

from copy import deepcopy

from slackbot.bot import Bot, listen_to

from . import numbers
from . import countdown_solver

# from .arithmetic.raw_parse import raw_parse
from .arithmetic import AvailableNumbers, parse

TARGET = None
NUMBERS = []
USER_STATES = {}


@listen_to("^.*give up.*$", re.IGNORECASE)
def solve_problem(message):
    if message.channel == "countingdown":
		try:
			result = countdown_solver.SolveProblem(TARGET, NUMBERS)
			message.reply("Result: {}".format(result))
		except Exception as e:
			message.reply("Problem: {}".format(e))


@listen_to("^([01234]) from the top.*$", re.IGNORECASE)
def chat_message(message, str_num_from_top_row):
    if message.channel == "countingdown":
		try:
			num_from_top_row = int(str_num_from_top_row)
		except (ValueError, TypeError):
			message.reply("Need a number between 0-4 from the top row")
			return

		return numbers_game(message, num_from_top_row)


@listen_to("^([\(\)0-9+/\*-= \n]*)$")
def user_statement(message, full_statement_str):
    if message.channel == "countingdown":
		for line in full_statement_str.split("\n"):
			statement = parse(line.strip())
			(available_numbers, target) = get_user_state(message.user)

			try:
				statement.evaluate(available_numbers)
			except Exception as e:
				message.reply("Problem: {}".format(e))
				break

			if target in available_numbers:
				message.reply("Congrats!")
				break
			else:
				message.reply("Yes: {}".format(statement))

			set_user_state(message.user, (available_numbers, target))


@listen_to("^reset$", re.IGNORECASE)
def reset(message):
    if message.channel == "countingdown":
		set_user_state(message.user, (AvailableNumbers(NUMBERS), TARGET))


def numbers_game(message, num_from_top_row):
    global NUMBERS
    global TARGET

    try:
        numbers_as_ints = numbers.pick_numbers(num_from_top_row)
    except ValueError as e:
        message.reply("Couldn't pick numbers: {0}".format(e))
        return
    numbers_as_strings = map(str, numbers_as_ints)

    target = numbers.generate_target()
    NUMBERS = numbers_as_ints
    TARGET = target
    set_user_state(message.user, (AvailableNumbers(NUMBERS), TARGET))
    for user_id in list(USER_STATES):
        del USER_STATES[user_id]

    response = "Target is {0} from {1}".format(
        target, ", ".join(numbers_as_strings)
    )
    message.reply(response)


def get_user_state(user):
    user_id = user["id"]

    if user_id not in USER_STATES:
        set_user_state(user, (AvailableNumbers(NUMBERS), TARGET))

    return USER_STATES[user_id]


def set_user_state(user, state):
    user_id = user["id"]
    print("setting to {}".format(state))
    USER_STATES[user_id] = state


def main():
    bot = Bot()
    bot.run()
