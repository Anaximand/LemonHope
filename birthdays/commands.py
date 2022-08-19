from datetime import datetime
from discord.ext import commands

from utils import CommandModule, getDBFromGuild
from birthdays.utils import saveBirthday, parseMonthDay

TABLE_NAME = 'birthday'

class Birthdays(CommandModule):
    def __init__(self, bot):
        CommandModule.__init__(self, bot)
        birthday_loop.start()


    @commands.command()
    async def birthday(self, ctx, *, args):

        birthday = parseMonthDay(args)
        if not birthday:
            return await ctx.channel.send('Oops! I couldn\'t understand that.')

        birthdaypocket = getDBFromGuild(str(ctx.message.guild)).table(TABLE_NAME)

        await saveBirthday(birthdaypocket, birthday, ctx.message.author.id)

        await ctx.message.channel.send('You\'re birthday is %s. Got it! *If I misunderstood, you can just tell me again!*' % birthday)

    @tasks.loop(hours=1)
    async def birthday_loop(self):
        today = datetime.now()
        # Just keep swimmin' if its not 1pm bot time
        if today.hour != 13:
            return

        for guild in self.bot.guild:
            birthdaypocket = getDBFromGuild(str(guild)).table(TABLE_NAME)
            birthdays = getBirthdaysOnDate(table, today)

            if len(birthdays) == 0:
                continue

            for birthday in birthdays:
                # figure out how to get channel to send too




async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Birthdays(bot))
