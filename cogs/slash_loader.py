import discord
from discord.ext import commands

class SlashLoader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.synced = False  # Ensure sync happens only once

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.synced:
            try:
                synced = await self.bot.tree.sync()
                print(f"✅ Synced {len(synced)} slash command(s).")
                self.synced = True
            except Exception as e:
                print(f"❌ Failed to sync slash commands: {e}")

async def setup(bot):
    await bot.add_cog(SlashLoader(bot))
