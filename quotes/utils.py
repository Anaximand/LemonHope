import re
from tinydb import Query

from utils import getGlobalSaveLock
from discord.abc import PrivateChannel

private_channel_quotes = os.getenv('private_channel_quotes').lower() == "true"

def isChannelPrivate(channel) -> bool:
    """
    Returns if a channel is private.
    Private channel quotes flag will always override this, allowing quotes to work in private channels
    """
    # Always return true if private channel quotes is enabled
    if private_channel_quotes:
        return True

    return isinstance(ctx.channel, PrivateChannel)

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


async def saveQuote(table, author, message, url, sendMessage):
    """
    saveQuote to db
    sendResponse is the send function from discord
    """
    async with getGlobalSaveLock():
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
