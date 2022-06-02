from asyncpg import Pool


async def run(db: Pool, guild_id: str, member_id: str):
    try:
        await db.execute("DELETE FROM session_uri WHERE guild_id = $1 AND user_id = $2", str(guild_id), str(member_id))
        await db.execute("DELETE FROM uri WHERE guild_id = $1 AND user_id = $2", str(guild_id), str(member_id))
        return True
    except Exception as e:
        return False