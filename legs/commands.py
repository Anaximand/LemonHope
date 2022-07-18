from discord.ext import commands
from discord.utils import get

BUTT_IS_LEGS = 'butt is legs'
BUTT_IS_NOT_LEGS = 'butt is not legs'
NO_BUTT_OR_LEGS = 'no butt or legs'

class Legs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()
        author = message.author
        guild = message.guild

        role_to_give = None

        if BUTT_IS_LEGS in content:
            role_to_give = BUTT_IS_LEGS

        if BUTT_IS_NOT_LEGS in content:
            role_to_give = BUTT_IS_NOT_LEGS

        if role_to_give:
            await self.removeRoles(guild, author)
            role = get(guild.roles, name=role_to_give)
            await author.add_roles(role)

        if NO_BUTT_OR_LEGS in content:
            await self.removeRoles(guild, author)

    async def removeRoles(self, guild, author):
        butt_is_legs = get(guild.roles, name=BUTT_IS_LEGS)
        butt_is_not_legs = get(guild.roles, name=BUTT_IS_NOT_LEGS)
        await author.remove_roles(butt_is_legs, butt_is_not_legs)


def setup(bot) -> None:
    """Load the Quotes cog."""
    bot.add_cog(Legs(bot))
