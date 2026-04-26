import discord
from discord.ext import commands
from discord import app_commands
from services.unmute_service import unmute_member

class Unmute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="unmute", description="Размьютить участника")
    @app_commands.describe(member="Участник для размьюта")
    @app_commands.guild_only()
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await unmute_member(interaction, member)

async def setup(bot: commands.Bot):
    await bot.add_cog(Unmute(bot))
