# Standard library imports:
from dataclasses import dataclass, field
from enum import Enum
from typing import List

# Local imports:
from .utils.typing import serializable
print("b")

# Mapping for server names from equivalencies to human-readable designations.
server_aliases = {
    "US": [
        "usw",
        "na",
    ],
    "EU": []
}

# Include server designations as idempotent lookups.
idempotent_mapping = dict(zip(*([list(server_aliases)] * 2)))

servers_dict = {
    # Include original designations.
    **idempotent_mapping,
    # Map each alias to its designation.
    **{
        alias: name
        for name, aliases in server_aliases.items()
        for alias in aliases
    },
}

Server = Enum("Server", idempotent_mapping)

ServerAliases = Enum("ServerAliases", servers_dict)


def fix_server(server):
    return Server[ServerAliases[server].value].value


@serializable
@dataclass(unsafe_hash=True)
class Game:
    # A globally unique ID for the game.
    unique_id: str = field(init=False)

    # The name of the game being hosted.
    name: str = field(compare=True)

    # The server that the game is being hosted on
    server: str = field(compare=True)

    # The timestamp that this game was first seen.
    created: int = field(compare=True)

    # The filename for the map being hosted.
    map: str

    # The username for the host of the game.
    host: str

    def __post_init__(self):
        self.server = fix_server(self.server)


@serializable
@dataclass(frozen=True)
class SubscriptionOptions:
    # The human-readable name used to refer to this subcription, which must
    # be unique to the channel the subscription is for.
    name: str

    # The pattern for the map filename this subscription filters for, if any.
    file_pattern: str = field(default=None)

    # The pattern for the game name this subscription filters for, if any.
    name_pattern: str = field(default=None)

    # The host realm(s) this subscription filters for, if any.
    servers: List[Server] = field(default_factory=list)

    def __post_init__(self):
        self.servers = list(map(fix_server, self.servers))


@serializable
@dataclass(frozen=True)
class SubscriptionContext:
    # The ID of the channel being subscribed to.
    channel_id: int

    # The ID of the user that created this subscription.
    creator_id: int = field(hash=False)


@dataclass
class SubscriptionKey:
    # A globally unique ID for the subscription.
    unique_id: str


@serializable
@dataclass(unsafe_hash=True)
class Subscription:
    # A globally unique ID for the subscription.
    unique_id: str = field(init=False)

    # The ID of the channel being subscribed to.
    channel_id: int

    # The ID of the user that created this subscription.
    creator_id: int = field(hash=False)

    # The provided options for the subsciption.
    options: SubscriptionOptions

    def __post_init__(self):
        self.unique_id = f"{self.channel_id}:{self.options.name}"
