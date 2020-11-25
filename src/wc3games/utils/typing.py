# Standard library imports:
from argparse import Action, SUPPRESS
from dataclasses import fields, make_dataclass
from functools import wraps
from io import StringIO
from itertools import chain
from operator import attrgetter

# Third-party imports:
from dataclass_factory import Factory
from discord.ext import commands
from simple_parsing import ArgumentParser, ParsingError

# The factory used to create dataclass instances.
factory = Factory()


# The parser used for serialization.
class Parser(ArgumentParser):
    # Block this parser from exiting.
    def exit(self, status=0, message=None):
        pass

    # Block this parser from printing usage unexpectedly.
    def error(self, status=0, message=None):
        raise ParsingError()


class HelpAction(Action):
    def __init__(self, *args, **kwargs):
        # Pass the arguments upwards, overriding nargs.
        super().__init__(*args, **{**kwargs, "nargs": 0})

    def __call__(self, *args, **kwargs):
        raise ParsingError()


# Augments a dataclass to include various serializations.
def serializable(cls):
    # Augment the given class.
    @wraps(cls, updated=())
    class Class(cls):
        # Create an argument parser specifically for this type.
        parser = Parser(prog=cls.__name__, add_help=False)

        # Add the sole argument for the parser.
        parser.add_arguments(cls, dest=cls.__name__)

        # Add a customized help command.
        parser.add_argument(
            "-h",
            "--help",
            action=HelpAction,
            default=SUPPRESS,
            help="show this help message",
        )

        @classmethod
        def load(cls, data):
            return factory.load(data, class_=cls)

        def dump(self):
            return factory.dump(self)

        @classmethod
        def parse(cls, args=None):
            # Parse, extract, and output the specified instance.
            return getattr(cls.parser.parse_args(args), cls.__name__)

        @classmethod
        async def convert(cls, context, text):
            # Split the singular argument.
            try:
                return cls.parse(text.split())
            except ParsingError as error:
                # Capture the usage into a string.
                cls.parser.print_help(usage := StringIO())

                # Relay the usage upwards.
                raise commands.CommandError(usage.getvalue()) from error

    # Output the augmented class.
    return Class


def combine(*classes, name="_dummy"):
    """
    Creates a new dataclass by combining the given classes.
    """
    # Combine the list of fields.
    combined = list(chain.from_iterable(map(fields, classes)))

    # Extract the name and type, as required by `make_dataclass`.
    cleaned = list(zip(
        *zip(*map(attrgetter("name", "type"), combined)),
        combined,
    ))
    list(map(print, cleaned))

    # Construct and output the class.
    return make_dataclass(name, cleaned)
