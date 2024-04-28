from datetime import datetime, timezone, timedelta, time
from discord.ext import commands, tasks

from utils import getDBFromGuild
from module import CommandModule, getSetting, isEnabled
from birthdays.utils import getBirthdaysOnDate, saveBirthday, parseMonthDay

utc = timezone.utc

# If no tzinfo is given then UTC is assumed.
timeToRun = time(hour=13, minute=0, tzinfo=utc)


class Birthdays(CommandModule):
    def __init__(self, bot):
        CommandModule.__init__(self, bot)
        self.registerModule(['channel'])
        self.task = self.birthday_loop.start()

    def cog_unload(self):
        self.birthday_loop.cancel()


    @commands.command()
    async def birthday(self, ctx, *args):
        if len(args) != 1:
            return await ctx.channel.send('If you\'d like you to tell me your birthday use "Lemon, birthday m/d"')

        birthday = parseMonthDay(args[0])
        if not birthday:
            return await ctx.channel.send('Oops! I couldn\'t understand that.')

        birthdaypocket = getDBFromGuild(str(ctx.message.guild)).table(self.TABLE_NAME)

        await saveBirthday(birthdaypocket, birthday, ctx.message.author.id)

        await ctx.message.channel.send('Your birthday is %s. Got it! *If I misunderstood, you can just tell me again!*' % birthday)

    @tasks.loop(time=timeToRun)
    async def birthday_loop(self):
        today = datetime.now()
        self.logger.info('Checking for birthdays on %s' % today)

        for guild in self.bot.guilds:
            # TODO - We shouldn't default to lists, this sucks
            isEnabled = (getSetting(guild, self.MODULE_NAME, 'enabled') or [None])[0]
            channelId = (getSetting(guild, self.MODULE_NAME, 'channel') or [None])[0]

            if not isEnabled or not channelId:
                continue

            birthdaypocket = getDBFromGuild(str(guild)).table(self.TABLE_NAME)
            birthdays = getBirthdaysOnDate(birthdaypocket, today)

            if len(birthdays) == 0:
                self.loggers.info('(%s) no birthdays found' % guild)
                continue

            channel = guild.get_channel(channelId)

            self.logger.info('(%s) Found %s birthdays' % (guild, len(birthdays)))

            for birthday in birthdays:
                # TODO custom message
                birthdayMessage = 'Happy Birthday %s!' % birthday.get('mention')
                await channel.send(birthdayMessage)

    @birthday_loop.before_loop
    async def before_birthday_loop(self):
        # Before running, ensure the bot is ready
        await self.bot.wait_until_ready()

async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Birthdays(bot))
