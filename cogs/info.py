import discord
from discord.ext import commands
import datetime
import platform
import psutil
import os

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="botinfo",
        aliases=["about", "vibecraft"],
        help="Display full information and stats about the VibeCraft bot."
    )
    async def botinfo(self, ctx):
        # Automatically get the owner using application info
        app_info = await self.bot.application_info()
        owner = app_info.owner

        now = datetime.datetime.now(datetime.UTC)
        start_time = getattr(self.bot, "start_time", now)
        uptime = now - start_time
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)

        total_users = sum(g.member_count for g in self.bot.guilds)
        total_guilds = len(self.bot.guilds)
        total_cogs = len(self.bot.cogs)

        # Memory and CPU usage
        process = psutil.Process(os.getpid())
        mem_usage = round(process.memory_info().rss / 1024 / 1024, 2)  # MB
        cpu_percent = process.cpu_percent(interval=0.5)

        embed = discord.Embed(
            title="🤖 VibeCraft Bot Information",
            description="Your all-in-one assistant for the **VibeCraft** community!",
            color=discord.Color.teal()
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        embed.add_field(name="👤 Creator", value=owner.mention if owner else "Unknown", inline=True)
        embed.add_field(name="📡 Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        embed.add_field(name="🕒 Started At", value=start_time.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=False)

        embed.add_field(name="📊 Servers", value=str(total_guilds), inline=True)
        embed.add_field(name="👥 Users", value=str(total_users), inline=True)
        embed.add_field(name="📦 Modules Loaded", value=str(total_cogs), inline=True)

        embed.add_field(name="⚙️ Prefix", value=f"`{ctx.prefix}`", inline=True)
        embed.add_field(name="🧠 Library", value=f"discord.py `{discord.__version__}`", inline=True)
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)

        embed.add_field(name="💾 Memory Usage", value=f"{mem_usage} MB", inline=True)
        embed.add_field(name="🧠 CPU Usage", value=f"{cpu_percent}%", inline=True)

        embed.add_field(
            name="🔗 GitHub",
            value="[View Source](https://github.com/S-SamarthBhatt-B/vibecraft-bot)",  # Update this
            inline=False
        )
        embed.add_field(
            name="📢 Invite Me",
            value="[Click here](https://discord.com/oauth2/authorize?client_id=1394527557193564210) to invite me!",  # Update this
            inline=False
        )

        embed.set_footer(text="Thanks for using VibeCraft ❤️ | Type !help to see available commands")

        await ctx.send(embed=embed)

# Setup
async def setup(bot):
    await bot.add_cog(Info(bot))
