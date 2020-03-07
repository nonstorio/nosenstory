import os
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def get_prefix(client, message):
    prefixes = ['', ',']
    if message.guild:
        prefixes = [',']
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(
    command_prefix = get_prefix,
    case_insensitive = True,
    owner_id = int(os.getenv('OWNER_ID')),
    description = 'NonStory (a.k.a. "Nonsensical Story") is an improvised party game where players answer given short questions, and as result their answers are composed in a brief nonsensical story which is fun to read!'
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}')
    polygon = bot.get_channel(int(os.getenv('POLYGON_CHANNEL_ID')))
    await polygon.send(
        content = f'Logged in: {datetime.now()}',
        delete_after = 10.0
    )
    return

bot.run(os.getenv('TOKEN'), bot = True, reconnect = True)
