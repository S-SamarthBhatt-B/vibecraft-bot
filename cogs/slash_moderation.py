import discord
from discord import app_commands
from discord.ext import commands

class SlashModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ /kick
    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member.mention} was kicked. Reason: `{reason}`")

    # ✅ /ban
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member.mention} was banned. Reason: `{reason}`")

    # ✅ /unban
    @app_commands.command(name="unban", description="Unban a user by ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"✅ Unbanned {user.mention}.")

    # ✅ /purge
    @app_commands.command(name="purge", description="Delete a number of messages in this channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"🧹 Deleted `{amount}` messages.", ephemeral=True)

    # ✅ /mute (uses timeout)
    @app_commands.command(name="mute", description="Mute a user for a number of minutes")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int):
        duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        await member.timeout(duration, reason=f"Muted by {interaction.user.display_name}")
        await interaction.response.send_message(f"🔇 Muted {member.mention} for `{minutes}` minutes.")

    # ✅ /unmute
    @app_commands.command(name="unmute", description="Remove timeout from a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"🔊 Unmuted {member.mention}.")

    # ✅ /lock
    @app_commands.command(name="lock", description="Lock the current channel for @everyone")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔒 Channel locked.")

    # ✅ /unlock
    @app_commands.command(name="unlock", description="Unlock the current channel for @everyone")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔓 Channel unlocked.")

    # ✅ /slowmode
    @app_commands.command(name="slowmode", description="Set slowmode delay for this channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"🐢 Slowmode set to `{seconds}` seconds.")

async def setup(bot):
    await bot.add_cog(SlashModeration(bot))