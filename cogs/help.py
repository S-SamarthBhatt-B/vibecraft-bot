import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Show all available commands.")
    async def help(self, ctx):
        embed = discord.Embed(
            title="🛠️ VibeCraft Help Menu",
            description="Here's a list of all my commands, organized by category:",
            color=discord.Color.from_str("#8E44AD")  # VibeCraft Purple
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            filtered_commands = [cmd for cmd in commands_list if not cmd.hidden]

            if filtered_commands:
                value = ""
                for command in filtered_commands:
                    aliases = f" (aliases: {', '.join(command.aliases)})" if command.aliases else ""
                    value += f"• `!{command.name}`{aliases} – {command.help or 'No description'}\n"
                embed.add_field(name=f"📂 {cog_name}", value=value, inline=False)

        embed.set_footer(text="Use the commands with the given prefix: !")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
