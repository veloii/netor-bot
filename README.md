# Netor Bot

This repo contains the API and Bot for Netor. There is another repo for the [dashboard](https://github.com/zelrdev/netor-web).

## Tech Stack

- [Python](https://python.org)
- [Heroku](https://heroku.com)
- [discord.py](https://github.com/Rapptz/discord.py)
- [PostgreSQL](https://postgresql.org)

## Development

- Install dependencies:

```sh
pip install -r requirements.txt
```

- Create a `.env`:

```
TOKEN="<discord bot token>"
APPLICATION_ID="<discord bot id>"
DATABASE_URL="database url from docker (created with dashboard setup), if in doubt use: 'postgresql://postgres:postgres@localhost:5432/postgres'"
WEB_URL="<dashbord url, if in doubt use 'http://localhost:3000'>"
SPECIAL_AUTH="<can be anything, must be the same for the bot and dashboard>"
PORT="<port for the api>"
```

- Start the bot:

```sh
py server.py
```
