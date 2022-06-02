from discord import app_commands
import discord
import os, sys

async def setup(client): 
    @client.tree.command()
    async def reload(interaction: discord.Interaction):
        try:
            for filename in os.listdir(f"./plugins"):
                if filename.endswith(".py"):
                    try:
                        await client.unload_extension(f"plugins.{filename[:-3]}")
                        await client.load_extension(f"plugins.{filename[:-3]}")
                    except:
                        await client.load_extension(f"plugins.{filename[:-3]}")
        except Exception as e:
            await interaction.response.send_message('{}: {}'.format(type(e).__name__, e))
        else:
            await interaction.response.send_message('\N{OK HAND SIGN}')