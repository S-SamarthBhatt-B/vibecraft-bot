import os
import json
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, UTC
import config

# Load environment variables from .env
load_dotenv()

# Get bot token
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ Bot token not found in .env file. Add TOKEN=...")

# Setup Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Create bot instance with multiple prefixes
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(*config.PREFIXES),
    intents=intents
)

# Remove the default help command so we can create our own
bot.remove_command("help")

# Track bot start time for uptime
bot.start_time = datetime.now(UTC)

# List of cogs to load
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

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

    # Save current guilds (server IDs) to JSON
    try:
        guild_ids = [str(g.id) for g in bot.guilds]
        with open("bot_guilds.json", "w") as f:
            json.dump(guild_ids, f)
        print(f"📁 Saved {len(guild_ids)} guild(s) to bot_guilds.json")
    except Exception as e:
        print(f"❌ Failed to save guilds: {e}")

# Load cogs/extensions
async def load_extensions():
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded extension: {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

# Main runner
async def main():
    await load_extensions()
    await bot.start(TOKEN)

# Run the bot
asyncio.run(main())
