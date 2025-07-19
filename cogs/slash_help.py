import discord
from discord.ext import commands
from discord import app_commands
import config

class SlashHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all commands and their uses")
    async def help(self, interaction: discord.Interaction):
        # Support multiple prefixes if needed
        prefix = config.PREFIXES[0] if isinstance(config.PREFIXES, list) else config.PREFIX

        embed = discord.Embed(
            title="📖 VibeCraft Help Menu",
            description="Here's a list of available commands.\n\nUse either **slash commands** (e.g. `/ping`) or prefix commands (e.g. `V!ping`).",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="📂 General",
            value=(
                f"`{prefix}ping` / `/ping` – Show bot latency\n"
                f"`{prefix}userinfo` / `/userinfo` – Show user info\n"
                f"`{prefix}serverinfo` / `/serverinfo` – Show server info\n"
                f"`{prefix}avatar` / `/avatar` – Show user's avatar\n"
                f"`{prefix}uptime` / `/uptime` – Show bot uptime"
            ),
            inline=False
        )

        embed.add_field(
            name="📂 Moderation",
            value=(
                f"`{prefix}kick` / `/kick` – Kick a user\n"
                f"`{prefix}ban` / `/ban` – Ban a user\n"
                f"`{prefix}unban` / `/unban` – Unban a user by ID\n"
                f"`{prefix}mute` / `/mute` – Mute a user\n"
                f"`{prefix}unmute` / `/unmute` – Unmute a user\n"
                f"`{prefix}warn` / `/warn` – Warn a user\n"
                f"`{prefix}warnings` / `/warnings` – Show user warnings\n"
                f"`{prefix}clearwarns` / `/clearwarns` – Clear warnings\n"
                f"`{prefix}lock` / `/lock` – Lock channel\n"
                f"`{prefix}unlock` / `/unlock` – Unlock channel\n"
                f"`{prefix}slowmode` / `/slowmode` – Set slowmode\n"
                f"`{prefix}purge` / `/purge` – Delete messages"
            ),
            inline=False
        )

        embed.add_field(
            name="📂 Info",
            value=(
                f"`{prefix}botinfo` / `/botinfo` – Show bot info\n"
                f"`{prefix}help` / `/help` – Show this help menu"
            ),
            inline=False
        )

        embed.set_footer(text="Made with ❤️ by VibeCraft | Try /help or V!help")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SlashHelp(bot))