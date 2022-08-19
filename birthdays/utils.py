from dateutil import parser
from tinydb import Query

from utils import getGlobalSaveLock

def parseMonthDay(datestr):
    monthDay = None

    try:
        datetime = parser.parse(datestr)
        return datetime.strftime('%m/%d')
    except:
        return None

async def saveBirthday(table, birthday, authorId):
    """
    save birthday to db
    """
    async with getGlobalSaveLock():
        bid = isAlreadySaved(table, birthday, authorId)
        if bid:
            table.update({'birthday': birthday}, doc_ids=[bid])
        else:
            table.insert({'author': authorId, 'birthday': birthday})


def isAlreadySaved(table, birthday, authorId):
    query = Query()
    results = table.search(query.author == authorId)

    try:
        singleResult = results[0]
    except IndexError:
        return False

    return singleResult.doc_id
