"""
groq.py - Implements a toxicity detector using the Groq.com API.

This module defines the GroqDetector class, which wraps the Groq.com language model
API for automated content moderation. It analyzes Discord messages and classifies
them as toxic or normal based on the system prompt instructions.
"""

from typing import Awaitable
import json

from loguru import logger
from groq import AsyncGroq

from .detector import AbstractDetector, Detection

DEFAULT_MODEL = "llama-3.3-70b-versatile"
with open("prompt/groq_system.txt", "r", encoding="utf-8") as f:
    DEFAULT_SYSTEM_PROMPT = f.read()

class GroqDetector(AbstractDetector):
    """
    GroqDetector is a toxicity detection class that uses the Groq.com language model API.

    This class wraps calls to the Groq API to perform content moderation on Discord messages.
    It implements the AbstractDetector interface, providing an `is_toxic` method that classifies
    messages as either toxic or normal using a system prompt defined in 'prompt/groq_system.txt'.
    """

    def __init__(self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        sys_prompt: str = DEFAULT_SYSTEM_PROMPT
    ) -> None:
        """
        Initialize the GroqDetector.

        Args:
            api_key (str): Your Groq.com API key.
            model (str): The language model to use (default: 'llama3-8b-8192').
            sys_prompt (str): The system prompt to use for moderation instructions.
        """

        self._client = AsyncGroq(api_key=api_key)
        self._model = model
        self._sys_prompt = sys_prompt

    async def is_toxic(self, msg: str) -> Awaitable[Detection]:
        """
        Analyze a Discord message for toxicity using the Groq API.

        Args:
            msg (Message): The Discord message object to analyze.

        Returns:
            Detection: A Detection object with the original message, a boolean indicating toxicity,
            and an optional score (not set by this implementation).

        Raises:
            ValueError: If the Groq API response format is unexpected.
        """

        logger.trace("Requesting moderation from Groq...")
        cplt = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                { "role": "system", "content": self._sys_prompt },
                { "role": "user", "content": msg }
            ]
        )

        res = str(cplt.choices[0].message.content)
        as_json = json.loads(res)

        if as_json["type"] == "normal":
            return Detection(message=msg, is_toxic=False)
        if as_json["type"] == "toxic":
            reason = as_json["reason"]
            return Detection(message=msg, is_toxic=True, reason=reason)

        raise ValueError("Unexpected response format", res)
