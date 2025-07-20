import discord
from discord.ext import commands
from discord import app_commands
import random

class SlashPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.instrumentals = [f"https://songs.vibecraft.sbs/songs/{i}.mp3" for i in range(1, 31)]
        self.vocals = [f"https://songs.vibecraft.sbs/songs/v{i}.mp3" for i in range(1, 21)]

    def pick_random_song(self):
        # Mix instrumental and vocal songs
        return random.choice(self.instrumentals + self.vocals)

    async def join_and_play(self, interaction: discord.Interaction, voice_channel):
        try:
            vc = await voice_channel.connect()
        except discord.ClientException:
            vc = discord.utils.get(self.bot.voice_clients, guild=voice_channel.guild)

        url = self.pick_random_song()
        vc.stop()
        vc.play(discord.FFmpegPCMAudio(url))

        await interaction.response.send_message(f"▶️ Now playing: `{url.split('/')[-1]}`")

    @app_commands.command(name="play", description="🎵 Play a random song from VibeCraft in your voice channel")
    async def play(self, interaction: discord.Interaction):
        if interaction.user.voice and interaction.user.voice.channel:
            await self.join_and_play(interaction, interaction.user.voice.channel)
        else:
            await interaction.response.send_message("❌ You must be in a voice channel to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashPlay(bot))
