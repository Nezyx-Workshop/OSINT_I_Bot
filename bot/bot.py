import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys and bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    """Event to print a message when the bot successfully logs in"""
    print(f'We have logged in as {bot.user}')

# Import the commands from osint_commands.py
# This allows us to separate our command logic into another file for clarity
from bot.commands import osint_commands

bot.run(TOKEN)
