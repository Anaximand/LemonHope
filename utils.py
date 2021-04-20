import asyncio

from tinydb import TinyDB

globalSaveLock = asyncio.Lock()

def getGlobalSaveLock():
    return globalSaveLock

def getDBFromGuild(guild):
    """
    Retrieves db from guild name
    Returns TinyDB db
    """
    return TinyDB(r'data/' + guild + r'.json')

