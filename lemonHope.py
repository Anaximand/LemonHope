import os
import logging

from discord.ext import commands
from dotenv import load_dotenv

import quotes.commands as quotes
import legs.commands as legs
import conversions.commands as conversions

logging.getLogger("discord").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run():
    logger.info('Lemon is starting')
    load_dotenv()
    token = os.getenv('lemonhope_token')

    lemon = commands.Bot(command_prefix="Lemon, ", log_handler=None)

    quotes.setup(lemon)
    legs.setup(lemon)
    conversions.setup(lemon)

    lemon.run(token)
    logger.info('Lemon has started')

run()
