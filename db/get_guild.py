from asyncpg import Pool

async def run(db: Pool, guild_id: str):
    try:
        guild = await db.fetchrow("SELECT * FROM guild WHERE id = $1", str(guild_id))
        return guild
    except:
        return False
