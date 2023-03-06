import random
import re

from discord.ext import commands
from tinydb import Query

from utils import CommandModule, getDBFromGuild
from quotes.utils import isAlreadyRemembered, saveQuote, getInt, shouldExcludeChannel

TABLE_NAME = 'quote'

class Quotes(CommandModule):
    def __init__(self, bot):
        CommandModule.__init__(self, bot)
        self.exclude = self.bot.config.get('exclude_channels')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Return early if private channel
        if shouldExcludeChannel(reaction.message.channel, self.exclude):
            return

        if str(reaction.emoji) == '💬' and not any(r.me is True for r in reaction.message.reactions):
            quotepocket = getDBFromGuild(str(reaction.message.guild)).table(TABLE_NAME)
            qid = await saveQuote(
                    quotepocket, reaction.message.author.name, reaction.message.content, reaction.message.attachments, reaction.message.jump_url, reaction.message.channel.send)
            self.logger.info('Saving quote #%d from %s via reaction', qid, reaction.message.author.name)

            await reaction.message.add_reaction('💬')


    @commands.command()
    async def remember(self, ctx, *, arg):
        # Return early if private channel
        if shouldExcludeChannel(ctx.channel, self.exclude):
            return await ctx.send('Sorry! I can\'t remember anything in this channel')

        split = arg.split(' ')

        name = split[0].lower()
        channel = ctx.message.channel
        findString = ''.join(split[1:]).lower()
        found = False

        messages = [message async for message in channel.history(limit=50)]
        quotepocket = getDBFromGuild(str(ctx.message.guild)).table(TABLE_NAME)

        for ms in messages:
            if name in ms.author.name.lower() and (findString in ms.content.lower() or not findString) and "Lemon, " not in ms.content:
                qid = await saveQuote(quotepocket, ms.author.name, ms.content, ms.attachments, ms.jump_url, ctx.send)
                self.logger.info('Saving quote #%d from %s via text command', qid, name)

                found = True
                break
        if not found:
            await ctx.send('Could not find a message from ' + name + ' containing "' + findString + '"')



    @commands.command()
    async def quote(self, ctx, *arg):
        quotepocket = getDBFromGuild(str(ctx.message.guild)).table(TABLE_NAME)

        # Parse query
        searchQuery = None
        try:
            searchQuery = arg[0]
        except IndexError:
            pass

        # Logic for number based searching
        numCapture, numQuery = [None, None]
        if searchQuery:
            numCapture = re.compile('#(\d+)')
            numQuery = numCapture.match(searchQuery)

        msg = None
        if len(arg) == 0:
            msg = random.choice(quotepocket.all())
        elif numQuery:
            msg = quotepocket.get(doc_id=int(numQuery.group(1)))
        else:
            query = Query()
            try:
                msg = random.choice(quotepocket.search(query.name.matches('.*' + searchQuery + '.*', flags=re.IGNORECASE)))
            except IndexError:
                msg = None

        if msg:
            url = msg.get('url')
            url = '' if not url else url

            await ctx.send('<%s> %s (#%d) %s' % (msg['name'], msg['message'], msg.doc_id, url))
        else:
            await ctx.send('Couldn\'t find that quote')


async def setup(bot) -> None:
    """Load the Quotes cog."""
    await bot.add_cog(Quotes(bot))
