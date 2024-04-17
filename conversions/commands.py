from discord.ext import commands
from conversions.utils import getConversionTupleFromMessage, convertMatch, buildConvertionStr

from module import CommandModule, isEnabled


class Conversions(CommandModule):
    def __init__(self, bot):
        CommandModule.__init__(self, bot)
        self.registerModule()

    @commands.Cog.listener()
    @isEnabled
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content = message.content

        matchTuples = getConversionTupleFromMessage(content)

        if len(matchTuples) == 0:
            return

        allConversions = list(map(convertMatch, matchTuples))
        allConversionsLen = len(allConversions)

        self.logger.info('Converting %d figures for %s', allConversionsLen, message.author.name)

        response = ''
        for idx, conversion in enumerate(allConversions):
            ogData, convertedData = conversion
            convStr = buildConvertionStr(ogData, convertedData)

            messageSegment = ''
            if allConversionsLen == 1 or idx == 0:
                messageSegment = convStr
            elif allConversionsLen - 1 == idx:
                comma = '' if allConversionsLen == 2 else ','
                messageSegment += '{comma} and {conversion}'.format(comma=comma, conversion=convStr)
            else:
                messageSegment = ', {conversion}'.format(conversion=convStr)

            response += messageSegment

        await message.reply(response, mention_author=False)


async def setup(bot) -> None:
    """Load the Conversions cog."""
    await bot.add_cog(Conversions(bot))
