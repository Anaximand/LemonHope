from utils import getGlobalSaveLock, getDBFromGuild
from settings import TABLE_NAME

import inspect
import logging
from discord.ext import commands
from tinydb import TinyDB, Query

class CommandModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Registering %s', self.__class__.__name__)

def getSetting(guild, module, setting):
    """
    Return a setting value, given a guild, module, and setting identifier
    """
    query = Query()
    db = getDBFromGuild(guild)
    results = db.table(TABLE_NAME).search(query.guild == guild and query.module == module and query.setting == setting)

    try:
        settingsResult = results[0]
    except IndexError:
        return None

    return settingsResult.get('value')

def isEnabled(module):
    def decorator(func):
        async def wrapper(ctx, *args):
            guild = ctx.guild or (ctx.message and ctx.message.guild)
            if (not getSetting(guild, module, 'enabled')):
                return False
            return func(ctx, *args);

        decorator.__name__ = func.__name__
        sig = inspect.signature(func)
        decorator.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])  # from ctx onward

        return wrapper
    return decorator
