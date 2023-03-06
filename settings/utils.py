
from utils import getGlobalSaveLock

async def getSetting(table, key):
    query = Query()
    results = await table.search(query.key == key)

    try:
        settingsResult = results[0]
    except IndexError:
        return False

    return settingsResult.value

async def saveSetting(table, key, value):
    async with getGlobalSaveLock():
        settingToSave = { 'key': key, 'value': value }

        query = Query()
        await table.upset(settingToSave, query.key == key)
