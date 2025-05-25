"""
bot.detector package initializer.

Exposes detector interfaces and the default GroqDetector implementation.
"""

from .detector import AbstractDetector, Detection
from .groq import GroqDetector
