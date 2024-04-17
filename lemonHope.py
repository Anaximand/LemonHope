import os
import logging
import asyncio

from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv

import quotes.commands as quotes
import legs.commands as legs
import conversions.commands as conversions
import help.commands as help
import settings.commands as settings
import birthdays.commands as birthdays

logging.getLogger("discord").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

intents = Intents(messages=True, message_content=True, reactions=True, members=True, guilds=True)

async def registerModules(lemon):
    await quotes.setup(lemon)
    await legs.setup(lemon)
    await conversions.setup(lemon)
    await help.setup(lemon)
    await settings.setup(lemon)
    await birthdays.setup(lemon)

def run():
    logger.info('Lemon is starting')
    load_dotenv()
    token = os.getenv('lemonhope_token')

    lemon = commands.Bot(command_prefix="Lemon, ", intents=intents, log_handler=None)

    # Register all modules during startup
    @lemon.event
    async def setup_hook():
        await registerModules(lemon)

    @lemon.event
    async def on_ready():
        logger.info('Lemon has started')

    lemon.run(token, log_level=logging.INFO)

run()
