import discord
from config import MODER_ID, HELPER_ID, LOG_CHANNEL_ID
from datetime import datetime, timezone

async def unmute_member(interaction: discord.Interaction, member: discord.Member):
    if not any(role.id in [MODER_ID, HELPER_ID] for role in interaction.user.roles):
        await interaction.response.send_message("У вас нет прав для размьюта.", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("У цели роль выше или равна вашей.", ephemeral=True)
        return

    try:
        await member.timeout(None)
    except discord.Forbidden:
        await interaction.response.send_message("Недостаточно прав для размьюта этого пользователя.", ephemeral=True)
        return

    embed = discord.Embed(title="Размьют пользователя", color=discord.Color.green())
    embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
    embed.add_field(name="Пользователь", value=member.mention, inline=False)
    embed.timestamp = datetime.now(timezone.utc)

    try:
        dm_embed = discord.Embed(title="Вас размьютили", color=discord.Color.green())
        dm_embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
        dm_embed.timestamp = datetime.now(timezone.utc)
        await member.send(embed=dm_embed)
    except Exception:
        pass

    await interaction.response.send_message(embed=embed, ephemeral=True)

    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
