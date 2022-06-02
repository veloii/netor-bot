import os
from discord.ext import commands
import asyncpg
import discord
from utils import default
from server import Client

intents = discord.Intents.all()

client = Client(intents=intents,
                application_id=os.environ['APPLICATION_ID'], db=None)


async def load_extensions(client: commands.Bot, path: str):
    for filename in os.listdir(f"./{path}"):
        if filename.endswith(".py"):
            print(f"{path}.{filename[:-3]}")
            await client.load_extension(f"{path}.{filename[:-3]}")


async def init():

    db = await asyncpg.create_pool(os.environ['DATABASE_URL'])
    client.db = db

    async with client:
        await load_extensions(client, "plugins")

        await client.start(os.environ['TOKEN'])

