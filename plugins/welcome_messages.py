from discord import RawMemberRemoveEvent, app_commands
import discord
import os, sys
from server import Client
from db import get_guild
from utils.default import format_discord_welcome

async def setup(client: Client): 
    @client.event
    async def on_raw_member_remove(payload: RawMemberRemoveEvent):
        try:
            db_guild = await get_guild.run(client.db, payload.guild_id)

            if db_guild['um_enabled']:
                if db_guild['um_leave_channel_id'] != "":
                    if db_guild['um_leave_msg'] != "":
                        channel = await client.fetch_channel(db_guild['um_leave_channel_id'])
                        await channel.send(format_discord_welcome(db_guild['um_leave_msg'], payload.user.guild, payload.user, channel))
                        
        except Exception as e:
            print(e)

    @client.event
    async def on_member_join(member: discord.Member):
        try:
            db_guild = await get_guild.run(client.db, member.guild.id)

            if db_guild['um_enabled']:
                if db_guild['um_welcome_channel_id'] != "":
                    if db_guild['um_welcome_msg'] != "":
                        channel = await client.fetch_channel(db_guild['um_welcome_channel_id'])
                        await channel.send(format_discord_welcome(db_guild['um_welcome_msg'], member.guild, member, channel))
                        
        except Exception as e:
            print(e)