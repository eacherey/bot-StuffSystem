import discord
from discord.ext import commands
import asyncio
from config import TOKEN
from services.db import init_db

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned,
                   intents=intents)

async def main():
    async with bot:
        await init_db()
        await bot.load_extension("cogs.ban")
        await bot.load_extension("cogs.mute")
        await bot.load_extension("cogs.unmute")
        await bot.load_extension("cogs.warn")
        await bot.load_extension("cogs.unwarn")
        await bot.load_extension("cogs.checkwarn")
        await bot.load_extension("cogs.member_tracker")
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    await bot.tree.sync()
    
    activity = discord.Activity(
        type=discord.ActivityType.custom,
        name="Наказывает Школьников",
        state="👀"
    )
    
    await bot.change_presence(activity=activity)
    
    print(f"{bot.user} has connected to Discord!")

if __name__ == '__main__':
    asyncio.run(main())
