"""
bot.py - Discord bot core class.

Defines the DiscordBot class, responsible for managing the Discord client,
adapting messages, and applying toxicity detection.
"""

from typing import List

from discord.message import Message
from discord import Client

from loguru import logger

from .detector import AbstractDetector
from .adapter import MessageAdapter
from .store import Store
from .store import Event

class DiscordBot:
    """
    The main Discord bot class that monitors channels for messages,
    adapts them using the provided adapter, and performs toxicity moderation.
    """

    def __init__(self,
        token: str,
        channels: List[str],
        detector: AbstractDetector,
        adapter: MessageAdapter,
        store: Store
    ) -> None:
        """
        Initialize the DiscordBot.

        Args:
            token (str): Discord API token.
            channels (List[str]): List of channel IDs to monitor.
            detector (AbstractDetector): Toxicity detector instance.
            adapter (MessageAdapter): Adapter for converting messages.
            store (Store): Store to push detections to.
        """

        self._client = Client()
        self._client.event(self.on_message)

        self._token = token
        self._channels = channels
        self._detector = detector
        self._adapter = adapter
        self._store = store

    async def run(self) -> None:
        """Run the Discord bot."""
        await self._client.start(token=self._token)

    async def on_message(self, msg: Message) -> None:
        """
        Event handler for new Discord messages.

        Args:
            msg (Message): The Discord message received.
        """

        raw_msg_logger = logger.bind(
            guild_name=msg.guild.name,
            guild_id=msg.guild.id,
            chan_name=msg.channel.name,
            chan_id=msg.channel.id,
            user_name=msg.author.name,
            user_id=msg.author.id,
            message=msg.clean_content
        )

        if str(msg.channel.id) not in self._channels:
            raw_msg_logger.trace("Received message from an unhandled channel")
            return

        try:
            raw_msg_logger.trace("Received message from handled channel, adapting")
            new_msg = self._adapter.get_message(msg)
            adp_msg_logger = raw_msg_logger.bind(
                adapted_user_id=new_msg.sender_id,
                adapted_user_name=new_msg.sender_name,
                adapted_message=new_msg.content
            )
        except Exception: # pylint: disable=broad-exception-caught
            raw_msg_logger.exception("Failed to adapt message")
            return

        try:
            adp_msg_logger.debug("Received message adapted, moderating")
            detection = await self._detector.is_toxic(new_msg.content)
            if detection.is_toxic:
                mod_logger = adp_msg_logger.bind(
                    mod_score=f"{detection.score:.2f}" if detection.score is not None else None,
                    mod_reason=detection.reason
                )

                mod_logger.warning("Message moderated, considered toxic")

            else:
                adp_msg_logger.debug("Message moderated, considered non-toxic")

            ev = Event(sender_id=new_msg.sender_id, sender_name=new_msg.sender_name,
                       detection=detection)
            await self._store.push_event(ev)

        except Exception: # pylint: disable=broad-exception-caught
            logger.exception("failed to get verdict")
            return
