from asyncpg import Pool


async def run(db: Pool, guild_id: str):
    try:
        guild = await db.fetch("SELECT * FROM guild WHERE id = $1", str(guild_id))
        return guild[0]["rtm_channel_id"]
    except:
        return False
