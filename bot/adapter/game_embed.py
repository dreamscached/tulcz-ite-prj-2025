"""
game_embed.py - Adapter for extracting message data from embedded Discord
game messages.
"""

import re
from discord import Message
from .adapter import MessageAdapter, MessageLike

RE_STEAM_ID = re.compile(r"\[(\d+)\]")

IDX_EMBED = 0
LEN_EMBED_GLOBAL = 4
LEN_EMBED_PM = 7

IDX_PM_SENDER_NAME = 0
IDX_PM_SENDER_ID = 1
IDX_PM_MESSAGE = 6

IDX_GLOBAL_SENDER_NAME = 0
IDX_GLOBAL_SENDER_ID  = 1
IDX_GLOBAL_MESSAGE = 3

class GameMessageEmbedAdapter(MessageAdapter):
    """
    Adapter for parsing and extracting relevant fields from a Discord Message embed
    representing game chat messages.
    """

    def get_message(self, msg: Message) -> MessageLike:
        """
        Extract a MessageLike from a game chat embed.

        Args:
            msg (Message): The Discord message containing the embed.

        Returns:
            MessageLike: The parsed message data.

        Raises:
            ValueError: If the embed structure is not recognized.
        """

        embed = msg.embeds[IDX_EMBED]

        if len(embed.fields) == LEN_EMBED_GLOBAL:
            sender_name = embed.fields[IDX_GLOBAL_SENDER_NAME].value
            sender_field = embed.fields[IDX_GLOBAL_SENDER_ID].value
            sender_id = extract_steam_id(sender_field)
            message = embed.fields[IDX_GLOBAL_MESSAGE].value
            return MessageLike(sender_name, sender_id, message)

        if len(embed.fields) == LEN_EMBED_PM:
            sender_name = embed.fields[IDX_PM_SENDER_NAME].value
            sender_field = embed.fields[IDX_PM_SENDER_ID].value
            sender_id = extract_steam_id(sender_field)
            message = embed.fields[IDX_PM_MESSAGE].value
            return MessageLike(sender_name, sender_id, message)

        raise ValueError(f"Expected embed of {LEN_EMBED_GLOBAL} or {LEN_EMBED_PM} fields")


def extract_steam_id(url: str) -> str:
    """
    Extracts a Steam ID from a URL or string using a regular expression.

    Args:
        url (str): The string potentially containing a Steam ID.

    Returns:
        str: The extracted Steam ID.

    Raises:
        ValueError: If no Steam ID is found.
    """

    if not (match := re.search(RE_STEAM_ID, url)):
        raise ValueError("No Steam ID in URL", url)
    return match.group(1)
