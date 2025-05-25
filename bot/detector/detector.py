"""
Abstract Detector Module

Defines the abstract base class for a toxicity detector and the Detection result type.
Intended for use with Discord messages.
"""

from typing import Protocol, Awaitable
from dataclasses import dataclass

@dataclass
class Detection:
    """
    Represents the result of a toxicity detection on a message.

    Attributes:
        message (str): The original message content that was analyzed.
        is_toxic (bool): Whether the message was detected as toxic.
        score (float | None): An optional confidence score or probability (e.g., from 0.0 to 1.0).
        reason (str | None): A reason for the given verdict (None if is_toxic=False)
    """

    message: str
    is_toxic: bool
    score: float | None = None
    reason: str | None = None

class AbstractDetector(Protocol): # pylint: disable=too-few-public-methods
    """
    Abstract base class for all toxicity detectors.

    Subclasses should implement the `is_toxic` method to analyze a Discord message.

    Methods:
        is_toxic(msg: Message) -> Detection:
            Analyze a Discord message for toxicity and return a Detection result.
    """

    async def is_toxic(self, msg: str) -> Awaitable[Detection]:
        """
        Analyze a Discord message and determine if it is toxic.

        Args:
            msg (Message): The Discord message object to be analyzed.

        Returns:
            Detection: The result of the toxicity analysis.
        """
