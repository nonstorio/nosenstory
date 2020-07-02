from os import getenv
from datetime import datetime
from discord.abc import GuildChannel
from discord.ext import commands
from ns.const import MISC
from .Context import Context

def get_prefix(client, message):
    from ns.models import NsGuild
    prefixes = [MISC.LONG_PREFIX]
    if message.guild:
        nsguild = NsGuild.get(NsGuild.ref_id == message.guild.id)
        prefixes.append(nsguild.prefix or MISC.SHORT_PREFIX)
    else:
        prefixes.extend([MISC.SHORT_PREFIX, ''])
    return commands.when_mentioned_or(*prefixes)(client, message)

class Bot(commands.Bot):
    extensions = [
        'ns.models',
        'ns.cogs.Mgmt'
    ]
    polygon: GuildChannel
    
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            case_insensitive = True,
            description = MISC.DESCRIPTION,
        )

        for ext in self.extensions:
            self.load_extension(ext)
        
        self.run(getenv('BOT_TOKEN'), bot = True, reconnect = True)
    
    async def on_ready(self):
        from ns import db
        from ns.models import NsGuild
        print(f'Logged in as {self.user.name}#{self.user.discriminator}')

        guilds_dict = [(guild.id,) for guild in self.guilds]
        NsGuild.insert_many(guilds_dict, fields = [NsGuild.ref_id]).on_conflict_ignore().execute()

        self.polygon = self.get_channel(int(getenv('POLYGON_CHANNEL_ID')))
        await self.polygon.send(f'Logged in at `{datetime.now()}`')
    
    async def on_message(self, message):
        ctx = await self.get_context(message, cls = Context)
        await self.invoke(ctx)

    async def on_guild_join(self, guild):
        from ns.models import NsGuild
        NsGuild.create(ref_id = guild.id)

    async def on_guild_remove(self, guild):
        from ns.models import NsGuild
        try:
            nsguild = NsGuild.get(NsGuild.ref_id == guild.id)
            nsguild.delete_instance(recursive = True)
        except: pass
    
    async def on_guild_channel_create(self, channel):
        from ns.models import NsGuild, NsChannel
        nsguild = NsGuild.get(NsGuild.ref_id == channel.guild.id)
        nschannel, new = NsChannel.get_or_create(
            ref_name = channel.name,
            guild = nsguild,
            defaults = {
                'ref_id': channel.id
            }
        )
        if not new:
            nschannel.ref_id = channel.id
            nschannel.save()
            await channel.send(f'I am reassigned to <#{channel.id}>, since channel with similar name was found in my database.')
    
    async def on_guild_channel_update(self, channel_old, channel):
        if channel_old.name == channel.name: return
        from ns.models import NsGuild, NsChannel
        nsguild = NsGuild.get(NsGuild.ref_id == channel.guild.id)
        nschannel = NsChannel.get_or_none(
            (NsChannel.ref_id == channel.id) |
            (NsChannel.ref_name == channel.name),
            NsChannel.guild == nsguild
        )
        if not nschannel: return
        if nschannel.ref_id == channel.id:
            nschannel.ref_name = channel.name
        else:
            nschannel.ref_id = channel.id
            await channel.send(f'I am reassigned to <#{channel.id}>, because channel with similar name was found in my database.')
        nschannel.save()
    
    async def on_guild_channel_delete(self, channel):
        from ns.models import NsGuild, NsChannel, NsMgmt
        nsguild = NsChannel.get(NsGuild.ref_id == channel.guild.id)
        nschannel = NsChannel.get_or_none(NsChannel.ref_id == channel.id)
        if not nschannel: return
        if nschannel.rounds_held == 0: return
        nsmgmt = NsMgmt.select(NsMgmt.user).distinct().where(
            (NsMgmt.guild == nsguild) |
            (NsMgmt.channel == nschannel)
        )
