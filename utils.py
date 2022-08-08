import logging
import asyncio

from discord.ext import commands
from tinydb import TinyDB

globalSaveLock = asyncio.Lock()

def getGlobalSaveLock():
    return globalSaveLock

def getDBFromGuild(guild):
    """
    Retrieves db from guild name
    Returns TinyDB db
    """
    return TinyDB(r'data/' + guild + r'.json')

class CommandModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Registering %s', self.__class__.__name__)
