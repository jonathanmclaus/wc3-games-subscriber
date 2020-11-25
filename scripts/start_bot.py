#!/usr/bin/env python3.8

# Standard library imports:
from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO

# Local imports:
from wc3games.bot import bot

logger = getLogger(__name__)

if __name__ == "__main__":
    # Parse the arguments.
    parser = ArgumentParser()
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    basicConfig(level=INFO)

    # Start the bot.
    bot.run(args.token)
