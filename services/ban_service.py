import discord
from config import MODER_ID, LOG_CHANNEL_ID
from datetime import datetime, timezone

async def ban_member(interaction: discord.Interaction, member: discord.Member, reason: str):
    if not any(MODER_ID == role.id for role in interaction.user.roles):
        await interaction.response.send_message("У вас нет прав для бана.", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("У цели роль выше или равна вашей.", ephemeral=True)
        return

    try:
        dm_embed = discord.Embed(title="Вы были забанены", color=discord.Color.red())
        dm_embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
        dm_embed.add_field(name="Причина", value=reason or "Не указана", inline=False)
        dm_embed.timestamp = datetime.now(timezone.utc)
        await member.send(embed=dm_embed)
    except Exception:
        pass

    try:
        await member.ban(reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message("Недостаточно прав для бана этого пользователя.", ephemeral=True)
        return

    embed = discord.Embed(title="Бан пользователя", color=discord.Color.red())
    embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
    embed.add_field(name="Пользователь", value=member.mention, inline=False)
    embed.add_field(name="Причина", value=reason or "Не указана", inline=False)
    embed.timestamp = datetime.now(timezone.utc)

    await interaction.response.send_message(embed=embed, ephemeral=True)

    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
