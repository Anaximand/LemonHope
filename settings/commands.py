from discord.ext import commands

from settings.utils import validateSetting, saveSetting, canMemberManage
from module import getSetting
from utils import getDBFromGuild, safeEval
from module import CommandModule

TABLE_NAME = 'settings'

class Settings(CommandModule):
    @commands.command()
    async def settings(self, ctx, *args):
        if not canMemberManage(ctx.author):
            ctx.send('Sorry! You do not have permission to manage settings')
        action = args[0]
        module = args[1]
        setting = args[2]

        if not action in ['get', 'set']:
            return await ctx.send('Invalid action')

        if not validateSetting(module, setting):
            return await ctx.send('No setting found')

        if action == 'get':
            settingValue = getSetting(ctx.message.guild, module, setting)
            return await ctx.send(settingValue)

        values = [safeEval(v.replace(',', '')) for v in args[3:]]

        await saveSetting(str(ctx.message.guild), module, setting, values)
        await ctx.send(values)

async def setup(bot) -> None:
    """Load the Settings cog."""
    await bot.add_cog(Settings(bot))
