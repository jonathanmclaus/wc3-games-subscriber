# Manages API related to computing which games are currently available.

# Standard-library imports:
from logging import getLogger
from typing import List

# Third-party imports:
from requests import get, codes
from boltons.dictutils import subdict

# Local imports:
from .types import Game

logger = getLogger(__name__)


def get_games() -> List[Game]:
    # Make the HTTP request used to fetch current games.
    response = get("https://api.wc3stats.com/gamelist")

    # Substitute an empty response in place of an invalid one.
    if response.status_code != codes.ok:
        logger.error("Response status code: %s", response.status_code)
        return []

    # Log the metadata.
    metadata = subdict(response.json(), drop=["body"])
    logger.info("Response metadata: %s", metadata)

    # Formalize and output the body.
    return list(map(Game, response.json()["body"]))
