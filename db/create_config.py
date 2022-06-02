from asyncpg import Pool
import uuid

async def run(db: Pool, guild_id: str, user_id: str):
    try:
        uri = str(uuid.uuid4())
        await db.execute('INSERT INTO uri (token, guild_id, user_id) VALUES ($1, $2, $3)', uri, str(guild_id), str(user_id))
        return uri
    except Exception as e:
        print(e)
        return False
