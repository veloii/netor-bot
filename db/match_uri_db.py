from asyncpg import Pool


async def run(db: Pool, guild_id: str, uri: str):
    try:
        uri_row = await db.fetchrow("SELECT * FROM session_uri WHERE guild_id = $1 AND token = $2", guild_id, uri)
        if uri_row:
            return uri_row
        else:
            return False
    except:
        return False
