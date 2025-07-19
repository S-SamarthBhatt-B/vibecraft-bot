import discord
from discord.ext import commands
from discord import app_commands
import config

class SlashHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all commands and their uses")
    async def help(self, interaction: discord.Interaction):
        prefix = config.PREFIX  # should be "V!"

        embed = discord.Embed(
            title="📖 VibeCraft Help",
            description="Here's a list of available commands:\n\n",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="📂 General",
            value=(
                f"{prefix}ping – Show bot latency\n"
                f"{prefix}userinfo – Show user info\n"
                f"{prefix}serverinfo – Show server info\n"
                f"{prefix}avatar – Show user's avatar\n"
                f"{prefix}uptime – Show bot uptime"
            ),
            inline=False
        )

        embed.add_field(
            name="📂 Moderation",
            value=(
                f"{prefix}kick – Kick a user\n"
                f"{prefix}ban – Ban a user\n"
                f"{prefix}unban – Unban a user by ID\n"
                f"{prefix}mute – Mute a user\n"
                f"{prefix}unmute – Unmute a user\n"
                f"{prefix}warn – Warn a user\n"
                f"{prefix}warnings – Show user warnings\n"
                f"{prefix}clearwarns – Clear user warnings\n"
                f"{prefix}lock – Lock a channel\n"
                f"{prefix}unlock – Unlock a channel\n"
                f"{prefix}slowmode – Set channel slowmode\n"
                f"{prefix}purge – Delete messages"
            ),
            inline=False
        )

        embed.add_field(
            name="📂 Info",
            value=(
                f"{prefix}botinfo – Show bot info\n"
                f"{prefix}help – Show this help menu"
            ),
            inline=False
        )

        embed.set_footer(text="Use slash commands too! Try /ping, /userinfo, etc.")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SlashHelp(bot))
