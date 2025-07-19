import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        prefix = ctx.prefix

        embed = discord.Embed(
            title="🛠️ VibeCraft Help Menu",
            description="Here's a list of all my commands, organized by category:",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        # Group commands by cog (category)
        categories = {}
        for command in self.bot.commands:
            if command.hidden:
                continue  # Skip hidden commands

            category = command.cog_name or "Other"
            if category not in categories:
                categories[category] = []
            
            aliases = f" (aliases: {', '.join(command.aliases)})" if command.aliases else ""
            description = command.help or "No description"
            formatted = f"`{prefix}{command.name}`{aliases} – {description}"
            categories[category].append(formatted)

        for category, cmds in categories.items():
            embed.add_field(
                name=f"📂 {category}",
                value="\n".join(cmds),
                inline=False
            )

        embed.set_footer(text=f"Use the commands with the given prefix: {prefix}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))