from discord.ext import commands

from utils import CommandModule, getDBFromGuild
from birthdays.utils import saveBirthday, parseMonthDay

TABLE_NAME = 'birthday'

class Birthdays(CommandModule):

    @commands.command()
    async def birthday(self, ctx, *, args):

        birthday = parseMonthDay(args)
        if not birthday:
            return await ctx.channel.send('Oops! I couldn\'t understand that.')

        birthdaypocket = getDBFromGuild(str(ctx.message.guild)).table(TABLE_NAME)

        await saveBirthday(birthdaypocket, birthday, ctx.message.author.id)

        await ctx.message.channel.send('You\'re birthday is %s. Got it! *If I misunderstood, you can just tell me again!*' % birthday)

async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Birthdays(bot))
