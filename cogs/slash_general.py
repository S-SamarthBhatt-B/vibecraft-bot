import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random

class SlashGeneral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ /ping
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: `{latency}ms`")

    # ✅ /userinfo
    @app_commands.command(name="userinfo", description="Get info about a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title="👤 User Information", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Username", value=str(member), inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        await interaction.response.send_message(embed=embed)

    # ✅ /serverinfo
    @app_commands.command(name="serverinfo", description="Get info about the current server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title="🌐 Server Information", color=discord.Color.green())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        await interaction.response.send_message(embed=embed)

    # ✅ /avatar
    @app_commands.command(name="avatar", description="Show a user's avatar")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        avatar_url = member.avatar.url if member.avatar else None
        if avatar_url:
            embed = discord.Embed(title=f"🖼️ {member.display_name}'s Avatar", color=discord.Color.purple())
            embed.set_image(url=avatar_url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ This user has no avatar.")

    # ✅ /uptime
    @app_commands.command(name="uptime", description="Check how long the bot has been online")
    async def uptime(self, interaction: discord.Interaction):
        now = datetime.datetime.now(datetime.UTC)
        start_time = getattr(self.bot, "start_time", None)

        if not start_time:
            await interaction.response.send_message("⚠️ Uptime not available. Bot start time not set.")
            return

        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(f"⏱ Bot Uptime: `{hours}h {minutes}m {seconds}s`")

async def setup(bot):
    await bot.add_cog(SlashGeneral(bot))
