from discord.ext import commands

TABLE_NAME = 'settings'

class Settings(CommandModule):

    @commands.command()
    async def settings(self, ctx, cmd, *args):
        print(cmd)
        print(args);


async def setup(bot) -> None:
    """Load the Settings cog."""
    bot.add_cog(Settings(bot))
