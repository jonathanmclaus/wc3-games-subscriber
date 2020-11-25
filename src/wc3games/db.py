# Standard library imports:
from logging import getLogger

# Third-party imports:
from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.sql import select

logger = getLogger()

metadata = MetaData()

# The engine is not instantiated immediately.
engine = None


subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("channel_id", Integer, nullable=False),
    Column("creator_id", Integer, nullable=False),
    Column("description", String, nullable=False),
    Column("name_pattern", String),
    Column("file_pattern", String),
    Column("servers", String),
)

games = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("server", String, nullable=False),
    Column("created", Integer, nullable=False),
    Column("map", String, nullable=False),
    Column("host", String, nullable=False),
    UniqueConstraint("name", "server", "created"),
)


messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message_id", Integer, nullable=False),
    Column("subscription_id", Integer),
    Column("game_id", Integer),
    ForeignKeyConstraint(
        ["subscription_id"],
        ["subscriptions.id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    ),
    ForeignKeyConstraint(
        ["game_id"],
        ["games.id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    ),
    UniqueConstraint("subscription_id", "game_id"),
)


def bind_engine(filepath=":memory:"):
    # Update the global variable directly.
    global engine

    # Create the appropriate engine, defaulting to an in-memory database.
    engine = create_engine(f"sqlite:///{filepath}", echo=True)

    # Instantiate the database.
    metadata.create_all(engine)


def create_subscription(conn, **kwargs):
    # Block duplicate subscriptions.
    conn.execute(subscriptions.insert(), **kwargs)


def get_subscriptions(conn):
    return list(map(dict, conn.execute(select([subscriptions]))))


def delete_subscriptions(conn):
    return list(map(dict, conn.execute(select([subscriptions]))))


# Create a default database.
bind_engine()
