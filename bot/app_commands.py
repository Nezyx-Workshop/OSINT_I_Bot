"""Commands related to the OSINT API interactions."""

import os
import requests
from discord.ext import commands

# Load the OSINT API key from environment variables
API_KEY = os.getenv("OSINT_API_KEY")

@commands.command(name="email")
async def search_email(ctx, *, email: str):
    """Searches for the provided email using the OSINT API."""
    await search_osint(ctx, 'email', email)

@commands.command(name="phone")
async def search_phone(ctx, *, phone: str):
    """Searches for the provided phone number using the OSINT API."""
    await search_osint(ctx, 'phone', phone)

async def search_osint(ctx, search_type, query):
    """Helper function to generalize the search on OSINT based on type and query."""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }
    url = f'https://osint.industries/search?type={search_type}&query={query}'
    response = requests.get(url, headers=headers, timeout=10)  # Added a timeout of 10 seconds

    if response.status_code == 200:
        data = response.json()
        await ctx.send(data['result'])
    else:
        await ctx.send(f'Error: {response.status_code}')

# Add the commands to the bot's command list
# This makes the commands available for users to call
def setup(bot):
    """Add the search commands to the bot instance."""
    bot.add_command(search_email)
    bot.add_command(search_phone)