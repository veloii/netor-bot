import discord
from server import Client
import os
from db import create_config
from discord import app_commands

async def setup(client: Client):

    @client.tree.command(name='config', description="Generates config URL for server")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    async def config(interaction: discord.Interaction):
        uri = await create_config.run(client.db, interaction.guild_id, interaction.user.id)

        if uri is False:
            embed = discord.Embed(description='Something went wrong', colour=0xFF0000)
        
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(description='Do NOT share this link with anyone else, one time use - link expires in 60 seconds', colour=0x5865f2)
        

        url = f"{os.environ['WEB_URL']}/{interaction.guild_id}/{uri}"

        url_view = discord.ui.View()
        url_view.add_item(discord.ui.Button(label='Config Link', style=discord.ButtonStyle.url, url=url))
    

        await interaction.response.send_message(embed=embed, view=url_view, ephemeral=True)

    