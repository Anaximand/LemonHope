from discord.ext import commands
from discord.utils import get
from random import choice

from module import CommandModule
from help import VERSION

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
        print(VERSION)
        await ctx.message.reply('I\'m running v%s. My source is here! %s' % (VERSION, SOURCE_URL));

    @commands.command()
    async def version(self, ctx):
        await ctx.message.reply('I\'m running v%s' % VERSION)

async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Help(bot))
