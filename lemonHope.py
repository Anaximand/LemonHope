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

def run():
    logger.info('Lemon is starting')
    load_dotenv()
    token = os.getenv('lemonhope_token')

    lemon = commands.Bot(command_prefix="Lemon, ", intents=intents, log_handler=None)

    # Todo - make a better config
    lemon.config = {}
    lemon.config['exclude_channels'] = [int(channel) for channel in (os.getenv('exclude_channels') or '').split(',') if channel != '']

    # Modules must be awaited, but the bot cant be in an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(registerModules(lemon))

    lemon.run(token)
    logger.info('Lemon has started')

run()
