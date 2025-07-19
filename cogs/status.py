import discord
from discord.ext import commands, tasks
import itertools

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ✅ Rotating status list
        self.statuses = itertools.cycle([
            # 🎮 Playing
            discord.Game("fun.vibecraft.sbs"),
            discord.Game("Minecraft Survival"),
            discord.Game("Visual Studio Code"),

            # 👀 Watching
            discord.Activity(type=discord.ActivityType.watching, name="over VibeCraft users"),
            discord.Activity(type=discord.ActivityType.watching, name="vibecraft.sbs"),

            # 🎧 Listening
            discord.Activity(type=discord.ActivityType.listening, name="your commands"),
            discord.Activity(type=discord.ActivityType.listening, name="song.vibecraft.sbs"),

            # 🎬 Streaming
            discord.Streaming(name="YT CHANNEL", url="https://www.youtube.com/@SoulBurner-290")
        ])

        self.switch_status.start()

    def cog_unload(self):
        self.switch_status.cancel()

    @tasks.loop(seconds=10)
    async def switch_status(self):
        await self.bot.change_presence(activity=next(self.statuses))

    @switch_status.before_loop
    async def before_switch_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Status(bot))
