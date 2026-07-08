import discord
from discord.ext import commands
from config import MEMBER_LOG_CHANNEL_ID


async def send_member_join(bot: commands.Bot, member: discord.Member):
    embed = discord.Embed(
        title="👋 Новый участник!",
        description=f"{member.mention} присоединился к нам!",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(
        name="📝 Имя",
        value=f"{member.name}#{member.discriminator}",
        inline=True
    )
    embed.add_field(
        name="🆔 ID",
        value=f"`{member.id}`",
        inline=True
    )
    embed.add_field(
        name="📅 Аккаунт создан",
        value=f"<t:{int(member.created_at.timestamp())}:D>",
        inline=True
    )

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    else:
        embed.set_thumbnail(url=member.default_avatar.url)

    embed.set_footer(text=f"ID: {member.id}")

    log_channel = bot.get_channel(MEMBER_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)

async def send_member_remove(bot: commands.Bot, member: discord.Member):
    embed = discord.Embed(
        title="🚪 Участник покинул сервер",
        description=f"{member.name} покинул нас...",
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(
        name="📝 Имя",
        value=f"{member.name}#{member.discriminator}",
        inline=True
    )
    embed.add_field(
        name="🆔 ID",
        value=f"`{member.id}`",
        inline=True
    )
    embed.add_field(
        name="⏳ Был на сервере",
        value=f"<t:{int(member.joined_at.timestamp())}:R>",
        inline=True
    )

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    else:
        embed.set_thumbnail(url=member.default_avatar.url)

    embed.set_footer(text=f"ID: {member.id}")

    log_channel = bot.get_channel(MEMBER_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
