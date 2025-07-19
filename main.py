import os
import json
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, UTC
import config

# Load .env file (contains TOKEN)
load_dotenv()

# Get token from environment
TOKEN = os.getenv("TOKEN")

# ✅ Check if token is found
if not TOKEN:
    raise ValueError("❌ Bot token not found in .env. Make sure you have TOKEN=...")

# Enable required Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # For userinfo/serverinfo

# Set up bot
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command("help")  # Remove default help command
bot.start_time = datetime.now(UTC)

# List of cogs (feature modules) to load
initial_extensions = [
    'cogs.general',
    'cogs.info',
    'cogs.help',
    'cogs.status',
    'cogs.moderation',

    # Slash command cogs
    'cogs.slash_general',
    'cogs.slash_info',
    'cogs.slash_help',
    'cogs.slash_moderation',
]

# Event: When bot is ready
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

    # Save bot's current guild IDs to a JSON file
    try:
        guild_ids = [str(g.id) for g in bot.guilds]
        with open("bot_guilds.json", "w") as f:
            json.dump(guild_ids, f)
        print(f"📁 Saved {len(guild_ids)} bot guilds to bot_guilds.json")
    except Exception as e:
        print(f"❌ Failed to save bot guilds: {e}")

# Load all cogs
async def load_extensions():
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded extension: {ext}")
        except Exception as e:
            print(f"❌ Failed to load extension {ext}: {e}")

# Run everything
async def main():
    await load_extensions()
    await bot.start(TOKEN)

# Start the bot
asyncio.run(main())
