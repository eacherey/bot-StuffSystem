import discord
from config import MODER_ID, HELPER_ID, LOG_CHANNEL_ID
from services.db import remove_warn, remove_all_warns
from datetime import datetime, timezone

async def unwarn_member(interaction: discord.Interaction, member: discord.Member, warn_id: int | None = None):
    if not any(role.id in [MODER_ID, HELPER_ID] for role in interaction.user.roles):
        await interaction.response.send_message("У вас нет прав для снятия варна.", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("У цели роль выше или равна вашей.", ephemeral=True)
        return

    if warn_id is not None:
        removed = await remove_warn(warn_id, member.id)
        if not removed:
            await interaction.response.send_message(
                f"Варн #{warn_id} не найден у {member.mention}.", ephemeral=True
            )
            return
        desc = f"Варн #{warn_id} снят с {member.mention}"
    else:
        count = await remove_all_warns(member.id)
        desc = f"Все варны ({count}) сняты с {member.mention}"

    embed = discord.Embed(title="Варн снят", description=desc, color=discord.Color.green())
    embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
    embed.timestamp = datetime.now(timezone.utc)

    await interaction.response.send_message(embed=embed, ephemeral=True)

    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
