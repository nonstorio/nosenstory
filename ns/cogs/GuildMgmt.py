import asyncio
import discord
import peewee
from discord import TextChannel
from discord.ext.commands import Cog, group, guild_only, has_permissions
from ns import db
from ns.const import EMOJI
from ns.models import NsGuild, NsChannel
from typing import Optional

class GuildMgmt(Cog, name = 'Guild Management'):
    @group()
    @guild_only()
    @has_permissions(manage_channels = True)
    async def channel(self, ctx):
        pass

    @channel.command(aliases = ['whitelist'])
    async def assign(self, ctx, channel: Optional[TextChannel]):
        """Whitelist a channel, so game can be run there"""
        channel = channel or ctx.message.channel
        nsguild, _ = NsGuild.get_or_create(ref_id = channel.guild.id)
        try:
            with db.atomic():
                NsChannel.create(
                    ref_id = channel.id,
                    ref_name = channel.name,
                    guild = nsguild
                )
        except peewee.IntegrityError:
            await ctx.send(f'<#{channel.id}> was already added to my database, <@{ctx.author.id}>.')
        else:
            await channel.send(f'<@{ctx.author.id}> Cool, now they can start game in <#{channel.id}>!')

def setup(bot):
    bot.add_cog(GuildMgmt())
