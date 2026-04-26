import discord
from services.db import get_warns
from datetime import datetime, timezone
from config import MODER_ID, HELPER_ID

async def checkwarn_member(interaction: discord.Interaction, member: discord.Member):
    if not any(role.id in [MODER_ID, HELPER_ID] for role in interaction.user.roles):
        await interaction.response.send_message("У вас нет прав для чекаварна.", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("У цели роль выше или равна вашей.", ephemeral=True)
        return

    warns = await get_warns(member.id)

    if not warns:
        await interaction.response.send_message(
            f"У {member.mention} нет активных варнов.", ephemeral=True
        )
        return

    embed = discord.Embed(
        title=f"Варны пользователя {member.display_name}",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    for warn in warns:
        mod = interaction.guild.get_member(warn["mod_id"])
        mod_str = mod.mention if mod else f"<@{warn['mod_id']}>"
        expires_ts = int(datetime.fromisoformat(warn["expires_at"]).timestamp())
        embed.add_field(
            name=f"Варн #{warn['id']}",
            value=f"**Модератор:** {mod_str}\n**Причина:** {warn['reason']}\n**Истекает:** <t:{expires_ts}:F>",
            inline=False
        )

    embed.set_footer(text=f"Всего варнов: {len(warns)}")
    embed.timestamp = datetime.now(timezone.utc)

    await interaction.response.send_message(embed=embed, ephemeral=True)
