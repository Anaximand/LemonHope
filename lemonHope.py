import os

from discord.ext import commands
from dotenv import load_dotenv

import quotes.commands as quotes

def run():
    print('Lemon is starting')
    load_dotenv()
    token = os.getenv('lemonhope_token')

    lemon = commands.Bot(command_prefix="Lemon, ")

    quotes.setup(lemon)

    lemon.run(token)

run()
