import os
import json
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, UTC
import config

# Load environment variables
load_dotenv()

# Get token
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ Bot token not found in .env. Make sure you have TOKEN=...")

# Enable intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for server info, user info, moderation

# Create bot instance
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Remove default help command (for custom one)
bot.remove_command("help")

# Track bot start time
bot.start_time = datetime.now(UTC)

# List of all cog modules to load
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

# When bot is ready
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")

    # Sync slash commands globally
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

    # Save list of server IDs the bot is in
    try:
        guild_ids = [str(g.id) for g in bot.guilds]
        with open("bot_guilds.json", "w") as f:
            json.dump(guild_ids, f)
        print(f"📁 Saved {len(guild_ids)} bot guilds to bot_guilds.json")
    except Exception as e:
        print(f"❌ Failed to save bot guilds: {e}")

# Load all extensions/cogs
async def load_extensions():
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded extension: {ext}")
        except Exception as e:
            print(f"❌ Failed to load extension {ext}: {e}")

# Run the bot
async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())
