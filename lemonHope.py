import random
import os
from discord.ext import commands
from tinydb import TinyDB, Query
from dotenv import load_dotenv
import asyncio
import re

print('Lemon is starting')
load_dotenv()
token = os.getenv('lemonhope_token')

lemon = commands.Bot(command_prefix="Lemon, ")


def getDBFromGuild(guild):
    return TinyDB(r'data/' + guild + r'.json')


def isAlreadyRemembered(table, author, msg):
    query = Query()
    return any(table.search(query.name.matches('.*' + author + '.*', flags=re.IGNORECASE) and query.message == msg))


async def saveQuote(table, author, message, sendResponse):
    if not isAlreadyRemembered(table, author, message):
        table.insert({'name': author, 'message': message})
        await sendResponse('Remembered that ' + author + ' said "' + message + '"')



@lemon.event
async def on_reaction_add(ctx, user):
    if str(ctx.emoji) == '💬' and not any(r.me is True for r in ctx.message.reactions):
        print('Saving quote from ' + ctx.message.author.name + ' via reaction')

        lock = asyncio.Lock()
        quotepocket = getDBFromGuild(str(ctx.message.guild)).table('quote')

        await lock.acquire()
        try:
            await saveQuote(
                    quotepocket, ctx.message.author.name, ctx.message.content, ctx.message.channel.send)
        finally:
            lock.release()

        await ctx.message.add_reaction('💬')


@lemon.command()
async def remember(ctx, *, arg):
    split = arg.split(' ')

    name = split[0]
    channel = ctx.message.channel
    findString = ''.join(split[1:])
    found = False

    print('Saving quote from ' + name + ' via text command')

    messages = await channel.history(limit=50).flatten()
    quotepocket = getDBFromGuild(str(ctx.message.guild)).table('quote')


    for ms in messages:
        if name in ms.author.name and (findString in ms.content or not findString) and "Lemon, " not in ms.content:
            lock = asyncio.Lock()
            await lock.acquire()
            try:
                await saveQuote(quotepocket, ms.author.name, ms.content, ctx.send)
            finally:
                lock.release()

            found = True
            break
    if not found:
        await ctx.send('Could not find a message from ' + name + ' containing "' + findString + '"')


@lemon.command()
async def quote(ctx, *arg):
    quotepocket = getDBFromGuild(str(ctx.message.guild)).table('quote')
    msg = None
    if len(arg) == 0:
        msg = random.choice(quotepocket.all())
    else:
        query = Query()
        msg = random.choice(quotepocket.search(query.name.matches('.*' + arg[0] + '.*', flags=re.IGNORECASE)))

    await ctx.send('<' + msg['name'] + '> ' + msg['message'])


lemon.run(token)
