import os
import re
from module import getSetting
from tinydb import Query

from utils import getGlobalSaveLock

def shouldExcludeChannel(guild, channel) -> bool:
    """
    Returns if a channel is excluded from quotes
    """
    excludes = getSetting(guild, 'quotes', 'exclude_channels') or []
    return channel.id in excludes

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


async def saveQuote(table, author, message, attachments, url, sendMessage):
    """
    saveQuote to db
    sendResponse is the send function from discord
    """
    async with getGlobalSaveLock():
        if len(attachments) != 0:
            message += ' ' + ' '.join([attachment.url for attachment in attachments if attachment.url]) or ''
        # qid is overloaded - but it gets the job done
        qid = isAlreadyRemembered(table, author, message)
        if not qid:
            qid = table.insert({'name': author, 'message': message, 'url': url})

        sentMessage = await sendMessage('Remembered that %s said "%s" (#%d) (%s)' % (author, message, qid, url))
        return qid


def getInt(s):
    """
    Get int - helper function
    Returns int or None
    """
    try:
        return int(s)
    except ValueError:
        return None
