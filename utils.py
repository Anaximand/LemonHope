import logging
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
    return TinyDB(r'data/' + str(guild) + r'.json')

def safeEval(val):
  """
  Safely runs an eval to convert strings to correct types automatically.
  Uses an empty built in dict to prevent function calls.
  Returns the original value if eval fails
  """
  builtins = { '__builtins__': None }
  try:
    return eval(val, builtins)
  except:
    return val
