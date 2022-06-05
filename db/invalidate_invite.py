from asyncpg import Pool

async def run(db: Pool, joined_id: str, guild_id: str):
    query = await db.fetch('SELECT * from user_invite WHERE joined_id = $1 AND guild_id = $2',
    str(joined_id),
    str(guild_id) 
    )

    if query.__len__() > 0:
        query.sort(key=lambda r: r['date_created'], reverse=True)
        query = query[0]
        await db.execute("UPDATE user_invite SET valid = $1 WHERE id = $2", False, query['id'])