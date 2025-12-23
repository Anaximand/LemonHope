from discord.ext import commands
from discord.utils import get

from module import CommandModule, isEnabled
from version import VERSION

class Version(CommandModule):
    def __init__(self, bot):
        CommandModule.__init__(self, bot)
        self.registerModule()

    @commands.command()
    @isEnabled
    async def version(self, ctx):
      await ctx.message.reply("I'm running v%s" % VERSION, mention_author=False)


async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Version(bot))
