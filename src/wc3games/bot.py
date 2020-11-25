# Standard library imports:
from itertools import product
from logging import getLogger

# Third-party imports:
from discord.ext import commands, tasks

# Local imports:
from wc3games.types import Subscription, SubscriptionOptions
from wc3games.games import get_games

# The singleton for the bot being managed.
bot = commands.Bot(command_prefix='$')

logger = getLogger(__name__)


@bot.event
async def on_command_error(context, error):
    await context.send(f"```{error}```")


@bot.command()
@commands.bot_has_permissions(send_messages=True)
@commands.check_any(
    # Block normal users from creating subscriptions.
    commands.has_permissions(manage_messages=True),
    # Allow anyone to create a subscription in DMs.
    commands.dm_only(),
)
async def subscribe(context, *, options: SubscriptionOptions):
    # Forward the new subscription to the registry.
    try:
        sub = (
            # Combine the context and options into a subscription.
            Subscription(
                channel_id=context.channel.id,
                creator_id=context.author.id,
                options=options,
            )
        )
    # Direct registration errors to the command handler.
    except ValueError as error:
        raise commands.CommandError(str(error))

    await context.send(f"Successfully registered subscription {sub}.")


@tasks.loop(seconds=5)
async def update():
    # Fetch the list of games prior.
    prior, after = set(get_games()), set(fetch_games())

    # Compute the sets of new, updated, and expired games.
    created = after - prior
    updated = after & prior
    expired = prior - after

    # Remove the state for any expired games.
    for game in expired:
        delete_messages(game)

    for game in updated:
        update_messages(game)

    for game in created:
        create_messages(game)


def delete_messages(game):
    # Look up the message IDs for the game.
    message_ids = get_message_ids(game)

    #  each message.
    for message_id in message_ids:
        message = bot.user.fetch_message(message_id)

        if game in expired:
            delete_message(message_id, game)
        else:
            update_message(message, game)
