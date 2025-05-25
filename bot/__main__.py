"""
Main entry point for the Discord toxicity moderation bot.

Initializes the GroqDetector, message adapter, and bot, then runs the bot.
"""

from asyncio import run
import sys

from redis.asyncio import Redis
from loguru import logger

from .detector import GroqDetector
from .adapter import GameMessageEmbedAdapter
from .bot import DiscordBot
from .store import Store
from . import config

logger.remove()
logger.add(sys.stderr, level="TRACE", format=(
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level> <white>{extra!r}</white>"
))

async def main():
    """
    Bootstraps and starts the Discord bot with toxicity moderation.
    """

    detector = GroqDetector(config.GROQ_API_TOKEN)
    adapter = GameMessageEmbedAdapter()
    store = Store(Redis.from_url(config.REDIS_CONN_URL))

    bot = DiscordBot(token=config.DISCORD_API_TOKEN,
                     channels=config.DISCORD_TARGET_CHANNELS,
                     detector=detector,
                     adapter=adapter,
                     store=store)

    logger.info("Starting DiscordBot...")
    await bot.run()

if __name__ == "__main__":
    run(main())
