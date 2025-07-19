import discord
from discord.ext import commands
import datetime
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ General Commands -------------------------

    @commands.command(name="ping", help="Check the bot's latency (response time).", aliases=["latency"])
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

    @commands.command(name="userinfo", help="Show information about a user.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title="👤 User Information",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Username", value=str(member), inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", help="Display details about this server.")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title="🌐 Server Information",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="avatar", help="Show the avatar of a user.", aliases=["pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        avatar_url = member.avatar.url if member.avatar else None
        if avatar_url:
            embed = discord.Embed(
                title=f"🖼️ {member.display_name}'s Avatar",
                color=discord.Color.purple()
            )
            embed.set_image(url=avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ This user has no avatar.")

    @commands.command(name="uptime", help="Show how long the bot has been online.")
    async def uptime(self, ctx):
        now = datetime.datetime.now(datetime.UTC)
        start_time = getattr(self.bot, "start_time", None)

        if not start_time:
            await ctx.send("⚠️ Uptime not available. Bot start time not set.")
            return

        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"⏱ Bot Uptime: `{hours}h {minutes}m {seconds}s`")

    # ✅ Message Listener -------------------------

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return  # Let command processing handle it

        content = message.content.lower().strip()
        guild = message.guild

        # 🎉 Greeting detection
        greetings = ["hi", "hello", "yo", "hey", "hii", "hola", "namaste", "sup"]
        if content in greetings:
            responses = [
                f"👋 Hey {message.author.display_name}! How's your day going?",
                f"🌟 Hello {message.author.display_name}, hope you're doing great!",
                f"😄 Yo {message.author.display_name}! Need anything?",
                f"👀 Sup {message.author.display_name}!",
                f"🙏 Namaste {message.author.display_name}! How can I help you?",
                f"Hey hey! {message.author.display_name}, what's up?",
                f"💬 Hello {message.author.display_name}! What are you working on?"
            ]
            await message.reply(random.choice(responses))
            return

        # 👑 Owner mention detection
        if guild.owner and guild.owner in message.mentions:
            await message.reply(f"👑 You mentioned the boss {guild.owner.display_name}! Need something?")
            return

        for role in message.role_mentions:
            if role.name.lower() == "owner":
                await message.reply("👑 You mentioned the @owner role! Everything okay?")
                return

        # ✅ Only process commands if nothing else matched
        await self.bot.process_commands(message)

# Setup
async def setup(bot):
    await bot.add_cog(General(bot))
