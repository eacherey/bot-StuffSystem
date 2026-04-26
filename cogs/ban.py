import discord
from discord.ext import commands
from discord import app_commands
from services.ban_service import ban_member

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Забанить участника")
    @app_commands.describe(member="Участник для бана", reason="Причина бана")
    @app_commands.guild_only()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Нарушение правил сервера"):
        await ban_member(interaction, member, reason)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))
