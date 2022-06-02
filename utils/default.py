import json
from discord.ext import commands
from discord import Guild
import discord

def config(filename: str = "config"):
    """ Fetch default config file """
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

from string import Formatter
from datetime import timedelta

def format_discord_welcome(message:str, guild: discord.Guild, member: discord.Member, channel: discord.abc.GuildChannel):
    return message.replace("@everyone", "").replace("@here", "").replace("^Server Name", guild.name).replace("^Mention User", f"<@{member.id}>").replace("^Username", member.display_name).replace("^Channel Name", channel.name).replace("^Mention Everyone", "@everyone").replace("^Mention Here", "@here")

def convert_embed_string_to_discord(embed_string: str):
    embed_json = json.loads(embed_string)

    embed = discord.Embed()

    if "title" in embed_json:
        embed.title = embed_json['title']

    if "description" in embed_json:
        embed.description = embed_json['description']

    if "url" in embed_json:
        embed.url = embed_json['url']

    if "color" in embed_json:
        embed.color = embed_json['color']
    
    if "footer" in embed_json:
        if "icon_url" in embed_json:
            embed.set_footer(text=embed_json['footer']['text'], icon_url=embed_json['footer']['icon_url'])
        else:
            embed.set_footer(text=embed_json['footer']['text'])

    if "image" in embed_json:
        if "url" in embed_json['image']:
            embed.set_image(url=embed_json['image']['url'])

    if "thumbnail" in embed_json:
        if "url" in embed_json['thumbnail']:
            embed.set_thumbnail(url=embed_json['thumbnail']['url'])

    if "author" in embed_json:
        if "name" in embed_json['author']:
            if "url" in embed_json['author']:
                if "icon_url" in embed_json['author']:
                    embed.set_author(name=embed_json['author']['name'], url=embed_json['author']['url'], icon_url=embed_json['author']['icon_url'])
                else:
                    embed.set_author(name=embed_json['author']['name'], url=embed_json['author']['url'],)
            else:
                if "icon_url" in embed_json['author']:
                    embed.set_author(name=embed_json['author']['name'], icon_url=embed_json['author']['icon_url'])
                else:
                    embed.set_author(name=embed_json['author']['name'])


    if "fields" in embed_json:
        for field in embed_json['fields']:
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

    return embed


def strfdelta(tdelta, fmt='{D:2} {H:2} {M:2} {S:2}', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can 
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the  
    default, which is a datetime.timedelta object.  Valid inputtype strings: 
        's', 'seconds', 
        'm', 'minutes', 
        'h', 'hours', 
        'd', 'days', 
        'w', 'weeks'
    """

    # Convert tdelta to integer seconds.
    if inputtype == 'timedelta':
        remainder = int(tdelta.total_seconds())
    elif inputtype in ['s', 'seconds']:
        remainder = int(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = int(tdelta)*60
    elif inputtype in ['h', 'hours']:
        remainder = int(tdelta)*3600
    elif inputtype in ['d', 'days']:
        remainder = int(tdelta)*86400
    elif inputtype in ['w', 'weeks']:
        remainder = int(tdelta)*604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('W', 'D', 'H', 'M', 'S')
    constants = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])

    return (f.format(fmt, **values))

def convert_error(error: Exception):
    if isinstance(error, discord.errors.Forbidden):
        return "Sorry, the bot does not have sufficient permissions"
    else:
        return str(error)