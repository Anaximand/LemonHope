from dateutil import parser
from tinydb import Query

from utils import getGlobalSaveLock

def formatDate(dt):
 return dt.strftime('%m/%d')

def parseMonthDay(datestr):
    try:
        dt = parser.parse(datestr)
        return formatBirthday(dt)
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

async def getBirthdaysOnDate(table, date):
    searchDate = formatDate(date)
    query = Query()

    return table.search(query.birthday == searchDate)

def isAlreadySaved(table, birthday, authorId):
    query = Query()
    results = table.search(query.author == authorId)

    try:
        singleResult = results[0]
    except IndexError:
        return False

    return singleResult.doc_id
