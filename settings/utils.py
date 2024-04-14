from utils import getGlobalSaveLock, getDBFromGuild
from settings import modules, TABLE_NAME

from tinydb import TinyDB, Query


def canMemberManage(member):
    isManager = member.guild_permissions.manage_guild or member.guild_permissions.administrator
    isLemonManager = member.roles and any(role.name == 'The Lemon Keeper' for role in member.roles)
    return isManager or isLemonManager

def validateSetting(module, setting):
    """
    Validate that a setting exists
    """
    if module not in modules:
        return False

    if setting not in modules[module]:
        return False

    return True

async def saveSetting(guild, module, setting, value):
    """
    Save settings, given a guild, module, and setting identifier
    """
    async with getGlobalSaveLock():
        db = getDBFromGuild(guild)
        settingToSave = { 'guild': guild, 'module': module, 'setting': setting, 'value': value }

        query = Query()
        db.table(TABLE_NAME).upsert(settingToSave, query.guild == guild and query.module == module and query.setting == setting)
