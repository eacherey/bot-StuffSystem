import discord
from discord.ext import commands
from discord import app_commands
from services.unwarn_service import unwarn_member

class Unwarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="unwarn", description="Снять варн с участника")
    @app_commands.describe(member="Участник", warn_id="ID варна (оставьте пустым чтобы снять все)")
    @app_commands.guild_only()
    async def unwarn(self, interaction: discord.Interaction, member: discord.Member, warn_id: int | None = None):
        await unwarn_member(interaction, member, warn_id)

async def setup(bot: commands.Bot):
    await bot.add_cog(Unwarn(bot))
