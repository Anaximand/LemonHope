from discord.ext import commands

from utils import CommandModule, getDBFromGuild


class Birthdays(CommandModule):

    @commands.command()
    async def birthday(self, ctx, birthday):
        print(ctx.message.author.mention, ctx.message.author.name)


async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Birthdays(bot))
