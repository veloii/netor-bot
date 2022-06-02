from db import check_rtm, get_rtm_channel
import discord
from server import Client

async def setup(client: Client):

    @client.tree.context_menu(name='Report to Moderators')
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        enabled = await check_rtm.run(client.db, interaction.guild_id)

        if not enabled:
            return await interaction.response.send_message("Sorry, this feature has not been enabled by server admins.", ephemeral=True)
        
        channel = await get_rtm_channel.run(client.db, interaction.guild_id)

        try:
            discord_channel = await interaction.guild.fetch_channel(channel)
        except:
            discord_channel = False

        if not discord_channel:
            return await interaction.response.send_message("Sorry, this feature has not been correctly configured by server admins.", ephemeral=True)

        # We're sending this response message with ephemeral=True, so only the command executor can see it
        await interaction.response.send_message(
            f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
        )

        embed = discord.Embed(title='Reported Message')
        if message.content:
            embed.description = message.content

        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.timestamp = message.created_at

        url_view = discord.ui.View()
        url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

        await discord_channel.send(embed=embed, view=url_view)

    