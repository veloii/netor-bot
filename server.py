import quart.flask_patch
from quart import Quart
from discord.ext import commands
import discord
import asyncio
from utils import setup
import os
from api import api
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ["PORT"]) | 4000
app = Quart(__name__)
app.register_blueprint(api)

class Client(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            application_id=kwargs.pop("application_id"),
            intents=kwargs.pop("intents"),
            command_prefix="-"
        )

        self.db = kwargs.pop("db")

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        self.loop.create_task(app.run_task('0.0.0.0', PORT, debug=True))
        await self.tree.sync(guild=MY_GUILD)


MY_GUILD = discord.Object(id=974939121028063262)

if __name__ == "__main__":
    asyncio.run(setup.init())