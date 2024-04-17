from utils import getGlobalSaveLock, getDBFromGuild
from settings import TABLE_NAME, registerModule

import inspect
import logging
from discord.ext import commands
from tinydb import TinyDB, Query

class CommandModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.MODULE_NAME = self.__class__.__name__.lower()
        self.TABLE_NAME = self.MODULE_NAME
        self.logger = logging.getLogger(self.MODULE_NAME)
        self.logger.info('Registering %s', self.MODULE_NAME)

    def registerModule(self, settings = []):
        return registerModule(self.MODULE_NAME, settings)

def isEnabled(func):
    """
    Checks if the module is currently enabled.
    If it's not enabled, the function will not be called.
    NOTE: Must be applied to each function in a CommandModule
    """
    async def decorator(self, ctx, *args, **kwargs):
        guild = ctx.guild or (ctx.message and ctx.message.guild)
        settingValues = getSetting(guild, self.MODULE_NAME, 'enabled')

        if (settingValues and not settingValues[0]):
            return

        await func(self, ctx, *args, **kwargs)

    decorator.__name__ = func.__name__
    sig = inspect.signature(func)
    decorator.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])  # from ctx onward
    return decorator

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
