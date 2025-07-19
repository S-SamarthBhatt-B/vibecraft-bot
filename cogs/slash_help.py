import discord
from discord import app_commands
from discord.ext import commands

class SlashHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all bot commands with descriptions")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 VibeCraft Help Menu",
            description="Here are all the available commands you can use:",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="⚙️ General",
            value="""
            **/ping** — Check the bot's latency
            **/userinfo** — Get info about a user
            **/serverinfo** — Get info about the server
            **/avatar** — View a user's avatar
            **/uptime** — See how long the bot has been online
            """,
            inline=False
        )

        embed.add_field(
            name="🧠 Info",
            value="""
            **/botinfo** — Show detailed bot stats and system info
            """,
            inline=False
        )

        embed.add_field(
            name="🔨 Moderation",
            value="""
            **/kick** — Kick a user from the server
            **/ban** — Ban a user
            **/unban** — Unban a user by ID
            **/warn** — Warn a user
            **/warnings** — View user warnings
            **/clearwarns** — Clear all warnings for a user
            **/purge** — Delete messages in bulk
            **/mute** — Mute a user
            **/unmute** — Unmute a user
            **/lock** — Lock a channel
            **/unlock** — Unlock a channel
            **/slowmode** — Enable slowmode in a channel
            """,
            inline=False
        )

        embed.set_footer(text="Need help? Contact VibeCraft Team 💜")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SlashHelp(bot))
