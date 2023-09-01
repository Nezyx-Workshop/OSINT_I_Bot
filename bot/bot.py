"""
This module sets up and runs the Discord bot.
"""

import os
from discord.ext import commands as discord_commands
from dotenv import load_dotenv
from app_commands import search_email, search_phone

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord_commands.Intents.default()
intents.message_content = True
bot = discord_commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event to print a message when the bot successfully logs in."""
    print(f'We have logged in as {bot.user}')

bot.add_command(search_email)
bot.add_command(search_phone)

bot.run(TOKEN)
