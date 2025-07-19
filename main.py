import os
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
intents.members = True  # Required for userinfo/serverinfo

# Set up bot
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# 🔥 Remove default help command to allow custom one
bot.remove_command("help")

# Store start time for uptime tracking
bot.start_time = datetime.now(UTC)

# Event: When bot is ready
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

# List of cogs (feature modules) to load
initial_extensions = [
    'cogs.general',
    'cogs.info',
    'cogs.help',
    'cogs.status',
    'cogs.moderation',
    'cogs.slash_loader',
    'cogs.slash_general',
    'cogs.slash_moderation',
    'cogs.slash_info',
    'cogs.slash_help',
    # Remove 'cogs.slash_loader' if no longer needed
]

# Load cogs
async def load_extensions():
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded extension: {ext}")
        except Exception as e:
            print(f"❌ Failed to load extension {ext}: {e}")

# Main runner
async def main():
    await load_extensions()
    await bot.start(TOKEN)

# Start the bot
asyncio.run(main())
