import discord
from discord.ext import commands
from services.member_tracker_service import send_member_remove, send_member_join

class MemberTracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await send_member_join(self.bot, member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await send_member_remove(self.bot, member)

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberTracker(bot))
