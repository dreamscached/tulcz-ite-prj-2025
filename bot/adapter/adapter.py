"""
adapter.py - Defines interfaces for adapting Discord messages into internal
representations.
"""

from typing import Protocol
from dataclasses import dataclass

from discord import Message

@dataclass
class MessageLike:
    """
    Represents a simplified version of a Discord message, containing only
    essential data.

    Attributes:
        sender_name (str): The display name of the message sender.
        sender_id (str): The unique identifier of the sender (could be a
            Steam ID or Discord ID).
        content (str): The content of the message.
    """

    sender_name: str
    sender_id: str
    content: str

class MessageAdapter(Protocol):
    """
    Protocol for objects that adapt Discord Message objects into MessageLike
    representations.
    """

    def get_message(self, msg: Message) -> MessageLike:
        """
        Convert a Discord Message into a MessageLike.

        Args:
            msg (Message): The Discord message to adapt.

        Returns:
            MessageLike: The adapted message.
        """
