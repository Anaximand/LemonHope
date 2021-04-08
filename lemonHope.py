import random
import os
from discord.ext import commands
from tinydb import TinyDB, Query
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('lemonhope_token')

lemon = commands.Bot(command_prefix="Lemon, ")
pants = TinyDB('data.json')
quotepocket = pants.table('quote')

@lemon.command()
async def remember(ctx, *arg):
    name = arg[0]
    channel = ctx.message.channel
    findString = ''.join(arg[1:])
    messages = await channel.history(limit=50).flatten()
    found = False
    for ms in messages:
        if ms.author.name == name and findString in ms.content and "Lemon, " not in ms.content:
            quotepocket.insert({'name': ms.author.name, 'message': ms.content})
            await ctx.send('Remembered that ' + ms.author.name + ' said "' +  ms.content + '"!')
            found = True
            break
    if not found:
        await ctx.send('Could not find a message from ' + name + ' containing ' + findString)

@lemon.command()
async def quote(ctx, *arg):
    if len(arg) == 0:
        msg = random.choice(quotepocket.all())
        await ctx.send('<' + msg['name'] + '> ' + msg['message'])
    else:
        query = Query()
        msg = random.choice(quotepocket.search(query.name == arg[0]))
        await ctx.send('<' + msg['name'] + '> ' + msg['message'])

lemon.run(token)


