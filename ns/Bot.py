import os
from datetime import datetime
from discord.abc import GuildChannel
from discord.ext import commands

def get_prefix(client, message):
    from ns.models import NsGuild
    prefixes = ['ns']
    if message.guild:
        nsguild = NsGuild.get_or_none(NsGuild.ref_id == message.guild.id)
        # Use custom guild prefix if set, substituting "comma" one
        prefixes.append(nsguild and nsguild.prefix or ',')
    else:
        prefixes.extend([',', ''])
    print(prefixes)
    return commands.when_mentioned_or(*prefixes)(client, message)

class Bot(commands.Bot):
    extensions = [
        'ns.models',
        'ns.cogs.GuildMgmt'
    ]
    polygon: GuildChannel
    
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            case_insensitive = True,
            owner_id = int(os.getenv('OWNER_ID')),
            description = 'NonStory (a.k.a. "Nonsensical Story") is an improvised party game where players answer given short questions, and as result their answers are composed in a brief nonsensical story which is fun to read!',
        )

        for ext in self.extensions:
            self.load_extension(ext)
        
        self.run(os.getenv('BOT_TOKEN'), bot = True, reconnect = True)
    
    async def on_ready(self):
        print(f'Logged in as {self.user.name}#{self.user.discriminator}')
        self.polygon = self.get_channel(int(os.getenv('POLYGON_CHANNEL_ID')))
        await self.polygon.send(f'Logged in at `{datetime.now()}`')
