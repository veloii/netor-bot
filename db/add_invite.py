from asyncpg import Pool
import uuid
from datetime import datetime, timedelta

from utils.default import strfdelta

async def run(db: Pool, guild_id: str, inviter_id: str, joined_id: str, invite_id: str):
    await db.execute('INSERT INTO user_invite (id, guild_id, inviter_id, joined_id, invite_id, valid, date_created) VALUES ($1, $2, $3, $4, $5, $6, $7)',
    str(uuid.uuid4()),
    str(guild_id),
    str(inviter_id),
    str(joined_id),
    str(invite_id),
    True,
    datetime.now()
    )