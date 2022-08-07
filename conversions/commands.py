from discord.ext import commands
from conversions.utils import getConversionTupleFromMessage, reMatchToTuple, convertMatch, buildConvertionSegment

class Conversions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content = message.content

        messageMatches = getConversionTupleFromMessage(content)
        matchTuples = list(map(reMatchToTuple, messageMatches))

        if len(matchTuples) == 0:
            return

        convStrs = []
        for idx, matchTuple in enumerate(matchTuples):
            convTuple = convertMatch(matchTuple)
            if not convTuple:
                continue

            convStrs.append(buildConvertionSegment(matchTuple, convTuple))

        if len(convStrs) == 0:
            return

        response = ''
        for idx, convStr in enumerate(convStrs):
            messageSegment = ''
            if len(convStrs) == 1 or idx == 0:
                messageSegment = convStr
            elif len(convStrs) - 1 == idx:
                comma = '' if len(convStrs) == 2 else ','
                messageSegment += '{comma} and {conversion}'.format(comma=comma, conversion=convStr)
            else:
                messageSegment = ', {conversion}'.format(conversion=convStr)

            response += messageSegment

        await message.channel.send(response)


def setup(bot) -> None:
    """Load the Quotes cog."""
    bot.add_cog(Conversions(bot))
