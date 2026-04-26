import discord
from discord.ext import commands
from discord import app_commands
from services.mute_service import mute_member

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Замьютить участника")
    @app_commands.describe(member="Участник для мута", duration="Время мута (например: 10m, 2h, 1d)", reason="Причина мута")
    @app_commands.guild_only()
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str | None = None):
        await mute_member(interaction, member, duration, reason)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))
