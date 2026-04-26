import discord
from discord.ext import commands
from discord import app_commands
from services.checkwarn_service import checkwarn_member

class Checkwarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="checkwarn", description="Посмотреть варны участника")
    @app_commands.describe(member="Участник")
    @app_commands.guild_only()
    async def checkwarn(self, interaction: discord.Interaction, member: discord.Member):
        await checkwarn_member(interaction, member)

async def setup(bot: commands.Bot):
    await bot.add_cog(Checkwarn(bot))
