import discord
from discord.ext import commands
from discord import app_commands
from services.warn_service import warn_member

class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Выдать варн участнику")
    @app_commands.describe(member="Участник", duration="Длительность (10m, 2h, 1d)", reason="Причина")
    @app_commands.guild_only()
    async def warn(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str):
        await warn_member(interaction, member, duration, reason)

async def setup(bot: commands.Bot):
    await bot.add_cog(Warn(bot))
