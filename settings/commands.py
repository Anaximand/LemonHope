from discord.ext import commands

from settings import modules
from settings.utils import validateSetting, saveSetting, canMemberManage, get_setting_spec
from module import getSetting
from utils import getDBFromGuild, safeEval
from module import CommandModule

TABLE_NAME = 'settings'

class Settings(CommandModule):
    @commands.command()
    async def settings(self, ctx, *args):
        if not canMemberManage(ctx.author):
            return await ctx.send('Sorry! You do not have permission to manage settings')
        if len(args) < 2:
            return await ctx.send(
                'Usage: `settings <get|set> <module> [setting] [values...]` — '
                'e.g. `settings get quotes` or `settings get quotes enabled` or `settings set quotes enabled true`'
            )
        action = args[0]
        module = args[1]
        setting = args[2] if len(args) >= 3 else None
        if action == 'set':
            if len(args) < 4:
                return await ctx.send('Usage: `settings set <module> <setting> <value> [value...]` — at least one value required')
        elif action != 'get':
            return await ctx.send('Invalid action')

        if module not in modules:
            return await ctx.send('No such module')

        if action == 'get':
            guild = ctx.message.guild
            if setting is None:
                lines = [f"**{module}** settings:"]
                for name in modules[module]:
                    value = getSetting(guild, module, name)
                    spec = get_setting_spec(module, name)
                    desc = f" — {spec.description}" if spec and spec.description else ""
                    lines.append(f"  **{name}**{desc}: `{value}`")
                return await ctx.send('\n'.join(lines))
            if not validateSetting(module, setting):
                return await ctx.send('No setting found')
            settingValue = getSetting(guild, module, setting)
            spec = get_setting_spec(module, setting)
            if spec and spec.description:
                msg = f"**{setting}** — {spec.description}. Value: `{settingValue}`"
            else:
                msg = str(settingValue)
            return await ctx.send(msg)

        if not validateSetting(module, setting):
            return await ctx.send('No setting found')
        values = [safeEval(v.replace(',', '')) for v in args[3:]]

        await saveSetting(str(ctx.message.guild), module, setting, values)
        spec = get_setting_spec(module, setting)
        if spec and spec.description:
            msg = f"Set **{setting}** — {spec.description}. New value: `{values}`"
        else:
            msg = str(values)
        await ctx.send(msg)

async def setup(bot) -> None:
    """Load the Settings cog."""
    await bot.add_cog(Settings(bot))
