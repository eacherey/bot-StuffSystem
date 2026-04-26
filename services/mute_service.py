import discord
from config import MODER_ID, HELPER_ID, LOG_CHANNEL_ID
from services.timeparse import get_until_from_now
from datetime import datetime, timezone

async def mute_member(interaction: discord.Interaction, member: discord.Member, duration_str: str, reason: str | None = None):
    if not any(role.id in [MODER_ID, HELPER_ID] for role in interaction.user.roles):
        await interaction.response.send_message("У вас нет прав для мута.", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("У цели роль выше или равна вашей.", ephemeral=True)
        return

    try:
        until = get_until_from_now(duration_str)
    except Exception as e:
        await interaction.response.send_message(f"Ошибка времени: {e}", ephemeral=True)
        return

    try:
        await member.timeout(until, reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message("Недостаточно прав для мута этого пользователя.", ephemeral=True)
        return

    embed = discord.Embed(title="Мут пользователя", color=discord.Color.orange())
    embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
    embed.add_field(name="Пользователь", value=member.mention, inline=False)
    embed.add_field(name="Причина", value=reason or "Не указана", inline=False)
    embed.add_field(name="Время", value=duration_str, inline=False)
    embed.timestamp = datetime.now(timezone.utc)

    try:
        dm_embed = discord.Embed(title="Вы были замьючены", color=discord.Color.orange())
        dm_embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
        dm_embed.add_field(name="Причина", value=reason or "Не указана", inline=False)
        dm_embed.add_field(name="Время", value=duration_str, inline=False)
        dm_embed.timestamp = datetime.now(timezone.utc)
        await member.send(embed=dm_embed)
    except Exception:
        pass

    await interaction.response.send_message(embed=embed, ephemeral=True)

    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
