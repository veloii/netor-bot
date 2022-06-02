from os import remove
from server import Client
import discord
from db import remove_member_uris
from datetime import datetime, timezone

async def setup(client: Client): 
    @client.event
    async def on_raw_member_remove(payload: discord.RawMemberRemoveEvent):
        await remove_uris(payload.user)

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        await check_user_permissions(after)

    @client.event
    async def on_guild_role_update(before: discord.Role, after: discord.Role):
        for member in after.members:
            await check_user_permissions(member)

    async def check_user_permissions(member: discord.Member):
        manage_guild = False
        for role in member.roles:
            if role.permissions.manage_guild:
                manage_guild = True
                break

        if member.guild.owner_id == member.id:
            return

        if not manage_guild:
            await remove_uris(member)
    
    async def remove_uris(member: discord.Member):
        guild_id = member.guild.id
        member_id = member.id
        await remove_member_uris.run(client.db, guild_id, member_id)