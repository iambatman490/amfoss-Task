import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database as db

# 1. Load token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2. Configure Intents (Required to read "!<command>" messages)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    db.init_db()  # Initialize database tables on startup
    print(f"⚓ The Berry Broker is active as {bot.user}!")

async def main():
    async with bot:
        # Load all modular cogs
        for cog in ["cogs.economy", "cogs.games", "cogs.fun"]:
            await bot.load_extension(cog)
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())