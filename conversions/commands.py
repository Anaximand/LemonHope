from discord.ext import commands
from conversions.utils import getConversionTupleFromMessage, convertMatch, buildConvertionStr

class Conversions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content = message.content

        matchTuples = getConversionTupleFromMessage(content)

        if len(matchTuples) == 0:
            return

        allConversions = list(map(convertMatch, matchTuples))
        allConversionsLen = len(allConversions)

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

        await message.channel.send(response)


def setup(bot) -> None:
    """Load the Quotes cog."""
    bot.add_cog(Conversions(bot))
