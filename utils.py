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


primitives = (bool, str, int, float, type(None))

def isPrimitive(obj):
    """
    Returns if an object is a "primative" type
    """
    return isinstance(obj, primitives)

def findAttribute(obj, target, depth=0):
    """
    Recursively searches for an attribute in an object
    """
    attrs = [attr for attr in dir(obj) if not attr.startswith('_')]

    # Guard against recursion issues
    if len(attrs) == 0 or depth > 5:
        return

    if target in attrs:
        return getattr(obj, target)

    for attr in attrs:
        attrObj = getattr(obj, attr)

        # Ignore "primative" types, they will cycle endlessly
        if isPrimitive(attrObj):
            continue

        potentialTarget = findAttribute(attrObj, target, depth+1)

        if potentialTarget:
            return potentialTarget
