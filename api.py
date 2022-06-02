import datetime
import os
import aiocache
from quart import Blueprint, Response, request, abort
from db import match_uri_db
import discord
from utils import setup as utils
from aiocache import cached
from aiocache.serializers import PickleSerializer
from utils.default import convert_embed_string_to_discord, convert_error
from db import add_punishment

cache = aiocache.Cache()

api = Blueprint('api', __name__)

async def setup(client):
    pass

def build_args(func, *args, **kwargs):
    ordered_kwargs = sorted(kwargs.items())

    return (
         (func.__module__ or "") + func.__name__ + str(args) + str(ordered_kwargs)
    )

@api.errorhandler(401)
def custom_401(error):
    return Response({"message": "Invalid authorization or guild id", "completed": False}, 401, {})

@cached(ttl=60, serializer=PickleSerializer())
async def get_guild_cache(guild: str):
    return await utils.client.http.get_guild(int(guild))

@api.get("/<guild>/get_guild")
async def get_guild(guild):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await get_guild_cache(guild)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@cached(ttl=60, serializer=PickleSerializer())
async def get_banned_members_cache(guild: str):
    return await utils.client.http.get_bans(int(guild), limit=1000, after=None)

@api.get("/<guild>/get_banned_members")
async def get_banned_members(guild: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await get_banned_members_cache(guild)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@cached(ttl=60, serializer=PickleSerializer())
async def get_members_cache(guild: str):
    return await utils.client.http.get_members(int(guild), limit=1000, after=None)

@api.get("/<guild>/get_members")
async def get_members(guild: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await get_members_cache(guild)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@cached(ttl=60, serializer=PickleSerializer())
async def get_roles_cache(guild: str):
    return await utils.client.http.get_roles(int(guild))

@api.get("/<guild>/get_roles")
async def get_roles(guild: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await get_roles_cache(guild)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@cached(ttl=60, serializer=PickleSerializer())
async def get_member_cache(guild: str, member_id: str):
    return await utils.client.http.get_member(int(guild), int(member_id))

@api.get("/<guild>/get_member/<member_id>")
async def get_member(guild: str, member_id: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await get_member_cache(guild, member_id)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@cached(ttl=60, serializer=PickleSerializer())
async def get_channels_cache(guild: str):
    return await utils.client.http.get_all_guild_channels(int(guild))

@api.get("/<guild>/get_channels")
async def get_channels(guild: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await get_channels_cache(guild)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@api.post("/<guild>/timeout_member/<member_id>/<reason>/<timestamp>")
async def timeout_member(guild: str, member_id: str, reason: str, timestamp: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)

    try:
        _guild = await utils.client.fetch_guild(guild)
        _member = await _guild.fetch_member(member_id)
        date = datetime.datetime.fromtimestamp(int(timestamp) / 1000).astimezone()
        now = datetime.datetime.now().astimezone()
        duration = date - now
        await _member.timeout(date, reason=reason)
        await add_punishment.run(utils.client.db, _guild.id, _member.id, valid["user_id"], "TIMEOUT", duration, reason)
        await cache.delete(build_args(get_member_cache, guild, member_id))
        return {"completed": True, "message": "OK", "result": True}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@api.post("/<guild>/ban_member/<member_id>/<reason>")
async def ban_member(guild: str, member_id: str, reason: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)

    try:
        _guild = await utils.client.fetch_guild(guild)
        _member = await _guild.fetch_member(member_id)
        await _member.ban(reason=reason)
        await add_punishment.run(utils.client.db, _guild.id, _member.id, valid["user_id"], "BAN", None, reason)
        await cache.delete(build_args(get_member_cache, guild, member_id))
        return {"completed": True, "message": "OK", "result": True}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}


@api.post("/<guild>/remove_member_ban/<member_id>")
async def remove_member_ban(guild: str, member_id: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        await utils.client.http.unban(member_id, guild)

        await cache.delete(build_args(get_member_cache, guild, member_id))
        return {"completed": True, "message": "OK", "result": True}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@api.get("/<guild>/get_member_ban/<member_id>")
async def get_member_ban(guild: str, member_id: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        req = await utils.client.http.get_ban(int(member_id), int(guild))
        return {"completed": True, "result": req}
    except Exception as e:
        if isinstance(e, discord.errors.NotFound):
            return {"completed": True, "result": None}
        return {"completed": False, "message": convert_error(e)}


@api.post("/<guild>/remove_member_timeout/<member_id>")
async def remove_member_timeout(guild: str, member_id: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        _guild = await utils.client.fetch_guild(guild)
        _member = await _guild.fetch_member(member_id)
        await _member.timeout(None)
        await cache.delete(build_args(get_member_cache, guild, member_id))
        return {"completed": True, "message": "OK", "result": True}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@api.post("/<guild>/send_message_embed/<channel_id>")
async def send_message_embed(guild: str, channel_id: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)
    try:
        _guild = await utils.client.fetch_guild(guild)
        channel = await _guild.fetch_channel(channel_id)
        form = await request.form
        embed_string = form.get("embed_string")
        embed = convert_embed_string_to_discord(embed_string) 
        await channel.send(embed=embed)
        return {"completed": True, "message": "OK", "result": True}
    except Exception as e:
        print(e)
        return {"completed": False, "message": convert_error(e)}

@api.post("/<guild>/kick_member/<member_id>/<reason>")
async def kick_member(guild: str, member_id: str, reason: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    if not valid:
        abort(401)

    try:
        _guild = await utils.client.fetch_guild(guild)
        _member = await _guild.fetch_member(member_id)
        await _member.kick(reason=reason)
        await add_punishment.run(utils.client.db, _guild.id, _member.id, valid["user_id"], "KICK", None, reason)
        await cache.delete(build_args(get_member_cache, guild, member_id))
        return {"completed": True, "message": "OK", "result": True}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}

@cached(ttl=60, serializer=PickleSerializer())
async def get_user_cache(user: str):
    return await utils.client.http.get_user(int(user))

@api.get("/<guild>/get_user/<user_id>")
async def get_user(guild: str, user_id: str):
    token = request.headers.get("Authorization")
    valid = await match_uri_db.run(utils.client.db, guild, token)
    special_auth = request.headers.get("Special-Authorization")
    special_valid = special_auth == os.environ['SPECIAL_AUTH']

    if not valid:
        abort(401)
    if not special_valid:
        abort(401)
    try:
        req = await get_user_cache(user_id)
        return {"completed": True, "result": req}
    except Exception as e:
        return {"completed": False, "message": convert_error(e)}
    