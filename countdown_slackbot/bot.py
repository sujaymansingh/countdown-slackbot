"""A bot to handle countdown games.

At the moment, it recognises only one pattern: '[01234] from the top'.

It could be extended by adding other patterns (e.g. 'inverted T' etc) that
then call `numbers_game` with the relevant number from the top.

This doesn't (yet) play any letters games or conundrums.
"""
import re

from slackbot.bot import Bot, listen_to

from countdown_slackbot import numbers


@listen_to("^([01234]) from the top.*$", re.IGNORECASE)
def chat_message(message, str_num_from_top_row):
    try:
        num_from_top_row = int(str_num_from_top_row)
    except (ValueError, TypeError):
        message.reply("Need a number between 0-4 from the top row")
        return

    return numbers_game(message, num_from_top_row)


def numbers_game(message, num_from_top_row):
    try:
        numbers_as_ints = numbers.pick_numbers(num_from_top_row)
    except ValueError as e:
        message.reply("Couldn't pick numbers: {0}".format(e))
        return
    numbers_as_strings = map(str, numbers_as_ints)

    target = numbers.generate_target()

    response = "Target is {0} from {1}".format(
        target, ", ".join(numbers_as_strings)
    )
    message.reply(response)


def main():
    bot = Bot()
    bot.run()
