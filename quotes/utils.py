import re
from tinydb import Query

from utils import getGlobalSaveLock

def isAlreadyRemembered(table, author, msg):
    """
    Determines if a quote already exists
    Returns None or quote document id
    """
    query = Query()
    results = table.search(query.name.matches('.*' + author + '.*', flags=re.IGNORECASE) and query.message == msg)

    try:
        singleResult = results[0]
    except IndexError:
        return False

    return singleResult.doc_id


async def saveQuote(table, author, message, sendResponse):
    """
    saveQuote to db
    sendResponse is the send function from discord
    """
    async with getGlobalSaveLock():
        # qid is overloaded - but it gets the job done
        qid = isAlreadyRemembered(table, author, message)
        if not qid:
            qid = table.insert({'name': author, 'message': message})
        await sendResponse('Remembered that ' + author + ' said "' + message + '" (#' + str(qid) + ')')


def getInt(s):
    """
    Get int - helper function
    Returns int or None
    """
    try:
        return int(s)
    except ValueError:
        return None
