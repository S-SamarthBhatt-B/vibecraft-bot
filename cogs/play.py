import discord
from discord.ext import commands
from discord import app_commands
import random

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.instrumentals = [f"https://songs.vibecraft.sbs/songs/{i}.mp3" for i in range(1, 31)]
        self.vocals = [f"https://songs.vibecraft.sbs/songs/v{i}.mp3" for i in range(1, 21)]

    def pick_random_song(self):
        # Mix instrumental and vocal songs
        return random.choice(self.instrumentals + self.vocals)

    async def join_and_play(self, interaction_or_ctx, voice_channel):
        try:
            vc = await voice_channel.connect()
        except discord.ClientException:
            vc = discord.utils.get(self.bot.voice_clients, guild=voice_channel.guild)

        url = self.pick_random_song()
        vc.stop()
        vc.play(discord.FFmpegPCMAudio(url))

        if isinstance(interaction_or_ctx, commands.Context):
            await interaction_or_ctx.send(f"▶️ Now playing: `{url.split('/')[-1]}`")
        else:
            await interaction_or_ctx.response.send_message(f"▶️ Now playing: `{url.split('/')[-1]}`")

    # Prefixed command: V!pms
    @commands.command(name="pms", help="Play a random song from VibeCraft in your voice channel.")
    async def pms_command(self, ctx):
        if ctx.author.voice:
            await self.join_and_play(ctx, ctx.author.voice.channel)
        else:
            await ctx.send("❌ You must be in a voice channel to use this command.")

    # Slash command: /pms
    @app_commands.command(name="pms", description="Play a random song from VibeCraft in your voice channel.")
    async def pms_slash(self, interaction: discord.Interaction):
        if interaction.user.voice:
            await self.join_and_play(interaction, interaction.user.voice.channel)
        else:
            await interaction.response.send_message("❌ You must be in a voice channel to use this command.", ephemeral=True)

    @pms_slash.error
    async def pms_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Something went wrong: " + str(error), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
