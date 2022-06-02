from discord.ext import commands
import os
import chalk
from db import match_uri_db
from server import Client


async def setup(client: Client):
    @client.event
    async def on_ready():
        print(chalk.bold(chalk.green(
            f'Logged in as {client.user} (ID: {client.user.id})')))
