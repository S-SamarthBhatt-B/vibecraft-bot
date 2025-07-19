import discord
from discord.ext import commands
import json
import os

WARN_FILE = "warns.json"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = self.load_warns()

    def load_warns(self):
        if os.path.exists(WARN_FILE):
            with open(WARN_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_warns(self):
        with open(WARN_FILE, "w") as f:
            json.dump(self.warns, f, indent=4)

    async def log_action(self, ctx, action, target: discord.Member, reason=None):
        log_channel = discord.utils.get(ctx.guild.text_channels, name="mod-logs")
        if not log_channel:
            log_channel = await ctx.guild.create_text_channel("mod-logs")
        embed = discord.Embed(
            title=f"🛡️ {action}",
            description=f"{target.mention} | `{target}`",
            color=discord.Color.orange()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        await log_channel.send(embed=embed)

    # ✅ Kick
    @commands.command(help="Kick a member from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} was kicked.")
        await self.log_action(ctx, "Kick", member, reason)

    # ✅ Ban
    @commands.command(help="Ban a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} was banned.")
        await self.log_action(ctx, "Ban", member, reason)

    # ✅ Unban
    @commands.command(help="Unban a user by username#tag or user ID.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user_input: str):
        bans = [entry async for entry in ctx.guild.bans()]
        user_input = user_input.strip()

        if user_input.isdigit():
            user_id = int(user_input)
            for entry in bans:
                if entry.user.id == user_id:
                    await ctx.guild.unban(entry.user)
                    await ctx.send(f"✅ Unbanned `{entry.user}`.")
                    await self.log_action(ctx, "Unban", entry.user)
                    return
            return await ctx.send("❌ No banned user with that ID.")

        if "#" in user_input:
            try:
                name, discriminator = user_input.split("#")
            except ValueError:
                return await ctx.send("⚠️ Use `name#tag` or ID.")
            for entry in bans:
                if entry.user.name == name and entry.user.discriminator == discriminator:
                    await ctx.guild.unban(entry.user)
                    await ctx.send(f"✅ Unbanned `{entry.user}`.")
                    await self.log_action(ctx, "Unban", entry.user)
                    return
            return await ctx.send("❌ No banned user with that tag.")

        await ctx.send("⚠️ Invalid input. Use `name#1234` or user ID.")

    # ✅ Purge
    @commands.command(help="Delete a number of messages in a channel.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        deleted = await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.", delete_after=3)

    # ✅ Mute
    @commands.command(help="Mute a member by adding a Muted role.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        await member.add_roles(muted_role)
        await ctx.send(f"🔇 {member.mention} has been muted.")
        await self.log_action(ctx, "Mute", member, reason)

    # ✅ Unmute
    @commands.command(help="Unmute a member by removing the Muted role.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"🔊 {member.mention} has been unmuted.")
            await self.log_action(ctx, "Unmute", member)

    # ✅ Warn
    @commands.command(help="Warn a member and save the reason.")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        self.warns.setdefault(guild_id, {})
        self.warns[guild_id].setdefault(user_id, [])
        self.warns[guild_id][user_id].append(reason or "No reason provided")
        self.save_warns()

        await ctx.send(f"⚠️ Warned {member.mention}")
        await self.log_action(ctx, "Warn", member, reason)

    # ✅ Warnings
    @commands.command(help="View all warnings of a member.")
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        warnings = self.warns.get(guild_id, {}).get(user_id, [])
        if not warnings:
            return await ctx.send(f"✅ {member.mention} has no warnings.")

        embed = discord.Embed(title=f"⚠️ Warnings for {member}", color=discord.Color.red())
        for i, warning in enumerate(warnings, 1):
            embed.add_field(name=f"Warning {i}", value=warning, inline=False)
        await ctx.send(embed=embed)

    # ✅ Clear Warnings
    @commands.command(help="Clear all warnings of a member.")
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if self.warns.get(guild_id, {}).pop(user_id, None):
            self.save_warns()
            await ctx.send(f"✅ Cleared all warnings for {member.mention}")
            await self.log_action(ctx, "Clear Warnings", member)
        else:
            await ctx.send(f"ℹ️ {member.mention} has no warnings to clear.")

    # ✅ Lock Channel
    @commands.command(help="Lock the current channel (deny sending messages).")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Channel locked.")

    # ✅ Unlock Channel
    @commands.command(help="Unlock the current channel.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Channel unlocked.")

    # ✅ Slowmode
    @commands.command(help="Set slowmode delay in the current channel.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds < 0 or seconds > 21600:
            return await ctx.send("⚠️ Time must be between 0–21600 seconds.")
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐢 Slowmode set to `{seconds}` seconds.")

# Setup
async def setup(bot):
    await bot.add_cog(Moderation(bot))