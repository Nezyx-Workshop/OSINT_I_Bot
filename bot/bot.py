"""
This module sets up and runs the Discord bot.
"""

import os
from discord.ext import commands
from dotenv import load_dotenv
from app_commands import search_email, search_phone
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event to print a message when the bot successfully logs in."""
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    """Event to handle errors triggered by commands."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry, I couldn't find the command: {ctx.message.content}")
    else:
        print(f"Unexpected error: {error}")

bot.add_command(search_email)
bot.add_command(search_phone)

bot.run(TOKEN)
