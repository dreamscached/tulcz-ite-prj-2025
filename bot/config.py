import os
from dotenv import load_dotenv

load_dotenv(".env.local")

DISCORD_API_TOKEN = os.environ["DISCORD_API_TOKEN"]
DISCORD_TARGET_CHANNELS = os.environ["DISCORD_TARGET_CHANNELS"].split(";")
GROQ_API_TOKEN = os.environ["GROQ_API_TOKEN"]
REDIS_CONN_URL = os.environ["REDIS_CONN_URL"]
