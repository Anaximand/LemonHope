
async def saveBirthday(table, author, birthday):
    """
    save birthday to db
    """
    async with getGlobalSaveLock():
        # qid is overloaded - but it gets the job done


async def isAlreadySaved(table, birthday, author):
    pass
