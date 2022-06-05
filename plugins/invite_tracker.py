# Copyright: GregTCLTK 2018-2021.
# Contact Developer on https://discord.gg/nPwjaJk (Skidder#8515 | 401817301919465482)
# Cog by: Quill (quillfires)

import discord
import asyncio
import json
import time
import typing
from db import add_invite, invalidate_invite
import datetime
from discord.ext import commands
# from discord.ext.commands import has_permissions
from discord import Embed

class invite_tracker(commands.Cog):
    """
    Keep track of your invites
    """
    def __init__(self, bot):
        self.bot = bot

        self.invites = {}
        bot.loop.create_task(self.load())

    async def load(self):
        await self.bot.wait_until_ready()
        # load the invites
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                await add_invite.run(self.bot.db, member.guild.id, invite.inviter.id, member.id, invite.id)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            await invalidate_invite.run(self.bot.db, member.id, member.guild.id)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            self.invites[guild.id] = await guild.invites()
        except:
            pass

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        try:
            self.invites[invite.guild.id].remove(invite)
        except:
            pass

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        try:
            self.invites[invite.guild.id].append(invite)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.invites.pop(guild.id)
        except:
            pass


async def setup(bot):
    await bot.add_cog(invite_tracker(bot))