from discord.ext import commands
from discord.utils import get
from random import choice

from module import CommandModule

SOURCE_URL = 'https://github.com/Anaximand/LemonHope/';
HI = [
    'Hi',
    'Hello',
    'Hola',
    'Bonjour',
    'Goddag',
    'שלום',
    'أهلا'
]

class Help(CommandModule):
    @commands.command()
    async def hi(self, ctx):
        await self.hello(ctx)

    @commands.command()
    async def hello(self, ctx):
        await ctx.message.reply('%s, %s!' % (choice(HI), ctx.message.author.mention))

    @commands.command()
    async def source(self, ctx):
        await ctx.message.reply('Here ya go! %s' % SOURCE_URL);

async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Help(bot))
