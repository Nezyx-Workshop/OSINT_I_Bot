"""Imports"""
import os
import asyncio
import aiohttp
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands

# Load the OSINT API key from environment variables
API_KEY = os.getenv("OSINT_API_KEY")
if not API_KEY:
    print("API Key not loaded")
else:
    print("API Key Loaded Successfully")

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
    print(f"Received {search_type} search request for query: {query}")

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'User-Agent': 'Mozilla/5.0'
    }

    url = f'https://osint.industries/api/{search_type}/{query}'
    print(f"Making request to {url} with headers {headers}")  # Debug statement to confirm URL and headers

    async with aiohttp.ClientSession() as session:
        for i in range(5):  # Retry mechanism (up to 5 retries)
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        data_entries = data.get('data', [])
                        
                        # Formatting the response data in a more compact and readable format
                        response_texts = []
                        for entry in data_entries:
                            module_data = entry.get('data', {})
                            module_response = [f"Module: {entry.get('module', 'Unknown')}", f"Query: {entry.get('query', {}).get('value', 'Unknown')}"]
                            for key, value in module_data.items():
                                if isinstance(value, dict):
                                    module_response.append(f"{key}: {', '.join([f'{k}: {v}' for k, v in value.items() if v])}")
                                else:
                                    module_response.append(f"{key}: {value}")
                            response_texts.append('\n'.join(module_response))

                        # Joining all responses and truncating if necessary
                        result = '\n\n'.join(response_texts)
                        if len(result) > 1000:
                            result = result[:1000] + "... (truncated)"
                        await ctx.send(result)
                        return
                    elif response.status == 401:
                        data = await response.json()
                        await ctx.send(f'Error: {response.status}, Response: {data["error"]}')
                        return
                    else:
                        response_text = await response.text()
                        await ctx.send(f'Error: {response.status}, Response: {response_text[:1000]}')  # Truncated to 1000 chars
                        return
            except aiohttp.ClientError as e:
                await ctx.send(f'Error: {str(e)}')
                return
            except Exception as e:
                print(f"Unexpected error on attempt {i+1}: {e}")
                await asyncio.sleep(2 ** i)  # Exponential backoff before retrying

def setup(bot):
    """Add the search commands to the bot instance."""
    bot.add_command(search_email)
    bot.add_command(search_phone)
