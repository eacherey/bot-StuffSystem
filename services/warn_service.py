import discord
from config import MODER_ID, HELPER_ID, LOG_CHANNEL_ID
from services.timeparse import get_until_from_now
from services.db import add_warn
from datetime import datetime, timezone

async def warn_member(interaction: discord.Interaction, member: discord.Member, duration_str: str, reason: str):
    if not any(role.id in [MODER_ID, HELPER_ID] for role in interaction.user.roles):
        await interaction.response.send_message("У вас нет прав для выдачи варна.", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("У цели роль выше или равна вашей.", ephemeral=True)
        return

    try:
        expires_at = get_until_from_now(duration_str)
    except Exception as e:
        await interaction.response.send_message(f"Ошибка времени: {e}", ephemeral=True)
        return

    warn_id = await add_warn(member.id, interaction.user.id, reason, expires_at)

    embed = discord.Embed(title="Варн выдан", color=discord.Color.yellow())
    embed.add_field(name="Пользователь", value=member.mention, inline=False)
    embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
    embed.add_field(name="Причина", value=reason, inline=False)
    embed.add_field(name="Истекает", value=f"<t:{int(expires_at.timestamp())}:F>", inline=False)
    embed.set_footer(text=f"Warn ID: {warn_id}")
    embed.timestamp = datetime.now(timezone.utc)

    try:
        dm_embed = discord.Embed(title="Вам выдан варн", color=discord.Color.yellow())
        dm_embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
        dm_embed.add_field(name="Причина", value=reason, inline=False)
        dm_embed.add_field(name="Истекает", value=f"<t:{int(expires_at.timestamp())}:F>", inline=False)
        dm_embed.timestamp = datetime.now(timezone.utc)
        await member.send(embed=dm_embed)
    except Exception:
        pass

    await interaction.response.send_message(embed=embed, ephemeral=True)

    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
