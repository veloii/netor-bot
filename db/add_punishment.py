from asyncpg import Pool
import uuid
from datetime import datetime, timedelta

from utils.default import strfdelta

async def run(db: Pool, guild_id: str, user_id: str, punisher_id: str, punishment: str, time: timedelta = None, reason: str = None):
    if reason is None:
        reason = "No reason specified"

    if time is None:
        time = ""
    else:
        time = strfdelta(time + timedelta(seconds=1))

    await db.execute('INSERT INTO punishment (id, user_id, guild_id, type, date, punisher_id, reason, time) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
    str(uuid.uuid4()),
    str(user_id),
    str(guild_id),
    punishment,
    datetime.now(),
    str(punisher_id),
    reason,
    time
    )