from discord import RawMemberRemoveEvent, app_commands
import discord
import os, sys
from db import add_punishment
from datetime import datetime, timezone

async def setup(client): 
    @client.event
    async def on_member_ban(guild: discord.Guild, user: discord.User):
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if user.id == entry.target.id:
                created_date = entry.created_at
                current_date = datetime.now(timezone.utc)

                if(current_date - created_date).seconds > 2:
                    if entry.user.id != client.user.id:
                        await add_punishment.run(client.db, guild.id, user.id, entry.user.id, "BAN", None, entry.reason)

    @client.event
    async def on_raw_member_remove(payload: RawMemberRemoveEvent):
        guild = await client.fetch_guild(payload.guild_id)
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if payload.user.id == entry.target.id:
                created_date = entry.created_at
                current_date = datetime.now(timezone.utc)

                if(current_date - created_date).seconds > 2:
                    if entry.user.id != client.user.id:
                        await add_punishment.run(client.db, payload.guild_id, payload.user.id, entry.user.id, "KICK", None, entry.reason)

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
            if after.id == entry.target.id:
                created_date = entry.created_at
                current_date = datetime.now(timezone.utc)

                if entry.changes.after.timed_out_until and not entry.changes.before.timed_out_until:
                    if(current_date - created_date).seconds > 2:
                        if entry.user.id != client.user.id:
                            date = entry.changes.after.timed_out_until
                            now = datetime.now()
                            duration = date - now
                            await add_punishment.run(client.db, after.guild.id, after.id, entry.user.id, "TIMEOUT", duration, entry.reason)

