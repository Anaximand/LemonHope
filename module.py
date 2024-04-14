import inspect
import logging
from discord.ext import commands

class CommandModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Registering %s', self.__class__.__name__)
