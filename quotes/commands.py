import random
import re

from discord.ext import commands
from tinydb import Query

from utils import CommandModule, getDBFromGuild
from quotes.utils import isAlreadyRemembered, saveQuote, getInt


class Quotes(CommandModule):

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == '💬' and not any(r.me is True for r in reaction.message.reactions):
            quotepocket = getDBFromGuild(str(reaction.message.guild)).table('quote')
            qid = await saveQuote(
                    quotepocket, reaction.message.author.name, reaction.message.content, reaction.message.channel.send)
            self.logger.info('Saving quote #%d from %s via reaction', qid, reaction.message.author.name)

            await reaction.message.add_reaction('💬')


    @commands.command()
    async def remember(self, ctx, *, arg):
        split = arg.split(' ')

        name = split[0].lower()
        channel = ctx.message.channel
        findString = ''.join(split[1:]).lower()
        found = False

        messages = await channel.history(limit=50).flatten()
        quotepocket = getDBFromGuild(str(ctx.message.guild)).table('quote')

        for ms in messages:
            if name in ms.author.name.lower() and (findString in ms.content.lower() or not findString) and "Lemon, " not in ms.content:
                qid = await saveQuote(quotepocket, ms.author.name, ms.content, ctx.send)
                self.logger.info('Saving quote #%d from %s via text command', qid, name)

                found = True
                break
        if not found:
            await ctx.send('Could not find a message from ' + name + ' containing "' + findString + '"')



    @commands.command()
    async def quote(self, ctx, *arg):
        quotepocket = getDBFromGuild(str(ctx.message.guild)).table('quote')

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
            await ctx.send('<' + msg['name'] + '> ' + msg['message'] + ' (#' + str(msg.doc_id) + ')')
        else:
            await ctx.send('Couldn\'t find that quote')


def setup(bot) -> None:
    """Load the Quotes cog."""
    bot.add_cog(Quotes(bot))
