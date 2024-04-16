from datetime import datetime
from discord.ext import commands, tasks

from utils import getDBFromGuild
from module import CommandModule, getSetting, isEnabled
from birthdays.utils import getBirthdaysOnDate, saveBirthday, parseMonthDay

TABLE_NAME = 'birthday'

class Birthdays(CommandModule):
    def __init__(self, bot):
        CommandModule.__init__(self, bot)
        self.registerModule(['channel'])
        self.task = self.birthday_loop.start()

    def cog_unload(self):
        self.birthday_loop.cancel()


    @commands.command()
    async def birthday(self, ctx, *args):
        birthday = parseMonthDay(args[0])
        print(args[0], birthday)
        if not birthday:
            return await ctx.channel.send('Oops! I couldn\'t understand that.')

        birthdaypocket = getDBFromGuild(str(ctx.message.guild)).table(TABLE_NAME)

        await saveBirthday(birthdaypocket, birthday, ctx.message.author.mention)

        await ctx.message.channel.send('Your birthday is %s. Got it! *If I misunderstood, you can just tell me again!*' % birthday)

    @birthday.error
    async def birthday_loop_error(self, error):
        print('error', error)

    @tasks.loop(seconds=10.0)
    async def birthday_loop(self):
        # This normally runs at 1pm bot time
        today = datetime.now()
        # Disabled for testing
        # Just keep swimmin' if its not 1pm bot time
        # if today.hour != 13:
            # return

        for guild in self.bot.guild:
            isEnabled = getSetting(guild, self.MODULE_NAME, 'enabled')
            channelId = getSetting(guild, self.MODULE_NAME, 'channel')
            if not isEnabled or not channelId:
                continue

            birthdaypocket = getDBFromGuild(str(guild)).table(TABLE_NAME)
            birthdays = getBirthdaysOnDate(birthdaypocket, today)

            if len(birthdays) == 0:
                continue

            channel = guild.get_channel(channelId)

            for birthday in birthdays:
                # figure out how to get channel to send too
                birthdayMessage = 'Happy Birthday %s!' % birthday.author
                await channel.send(birthdayMessage)

    @birthday_loop.before_loop
    async def before_birthday_loop(self):
        # This wait isn't finishing
        await self.bot.wait_until_ready()

async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Birthdays(bot))
