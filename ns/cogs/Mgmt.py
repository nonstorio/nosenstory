import asyncio
import discord
import peewee
from discord import Embed, TextChannel
from discord.ext.commands import Cog, CheckFailure, UserInputError, group, guild_only, check
from ns import db
from ns.const import COLOUR, EMOJI, MISC
from ns.models import NsGuild, NsChannel, NsMgmt
from typing import Optional

async def mgmt_guild(ctx):
    if ctx.author.permissions_in(ctx.channel).administrator: return True
    try:
        NsMgmt.get(
            NsMgmt.user == ctx.author.id,
            NsMgmt.guild == ctx.guild.id
        )
    except:
        raise CheckFailure(f'You do not have {MISC.COG_MGMT} permissions for guild.')
    return True

async def mgmt_channel(ctx):
    if ctx.author.permissions_in(ctx.channel).administrator: return True
    try:
        NsMgmt.get(
            NsMgmt.user == ctx.author.id,
            (NsMgmt.guild == ctx.guild.id) | (NsMgmt.channel == ctx.channel.id)
        )
    except:
        raise CheckFailure(f'You do not have {MISC.COG_MGMT} permissions for channel or guild.')
    return True

class Mgmt(Cog, name = MISC.COG_MGMT):
    @group(invoke_without_command = True, aliases = ['server'])
    @guild_only()
    async def guild(self, ctx):
        '''Game data for guild.'''
        nsguild = NsGuild.get(NsGuild.ref_id == ctx.guild.id)
        prefix = nsguild.prefix or MISC.SHORT_PREFIX
        embed = Embed(title = ctx.guild.name, colour = COLOUR.PRIMARY)
        embed.set_thumbnail(url = ctx.guild.icon_url_as(size = 64))
        embed.add_field(name = 'Guild NSID', value = f'`{nsguild.id}`')
        embed.add_field(name = 'Prefix', value = f'`{prefix}`')
        if nsguild:
            total_chan = NsChannel.select().where(NsChannel.guild == nsguild).count()
            embed.add_field(name = 'Total game channels', value = f'`{total_chan}`')
        await ctx.reply(embed = embed)

    @guild.command()
    @check(mgmt_guild)
    async def prefix(self, ctx, prefix: str):
        '''Use custom single character prefix for bot commands in guild instead of default.'''
        nsguild = NsGuild.get(NsGuild.ref_id == ctx.guild.id)
        if len(prefix) != 1:
            raise UserInputError('Custom prefix must consist of single character.')
        await ctx.send(f'<@{ctx.author.id}> Now I will react to commands after "`{prefix}`": details in `{prefix}help`.')
        if prefix == MISC.SHORT_PREFIX:
            prefix = None
        nsguild.prefix = prefix
        nsguild.save()

    @group(invoke_without_command = True, aliases = ['chan'])
    @guild_only()
    async def channel(self, ctx, channel: Optional[TextChannel]):
        '''Game data for channel.'''
        channel = channel or ctx.message.channel
        nschannel = NsChannel.get_or_none(NsChannel.ref_id == channel.id)
        nsid = nschannel and nschannel.id or 'n/a'
        embed = Embed(title = f'#{channel.name}', colour = nschannel and COLOUR.PRIMARY or COLOUR.SECONDARY)
        embed.set_thumbnail(url = ctx.guild.icon_url_as(size = 64))
        embed.add_field(name = 'Channel NSID', value = f'`{nsid}`')
        if nschannel:
            embed.add_field(name = 'Rounds held', value = f'`{nschannel.rounds_held}`')
        await ctx.reply(embed = embed)

    @channel.command(aliases = ['add'])
    @check(mgmt_guild)
    async def assign(self, ctx, channel: Optional[TextChannel]):
        '''Assign bot to a channel, so game can be run there.'''
        channel = channel or ctx.message.channel
        nsguild = NsGuild.get(NsGuild.ref_id == ctx.guild.id)
        _, created = NsChannel.get_or_create(
            ref_id = channel.id,
            ref_name = channel.name,
            guild = nsguild
        )
        if created:
            await ctx.reply(f'I am now assigned to <#{channel.id}>. Happy play!')
        else:
            await ctx.reply(f'Channel <#{channel.id}> is already in my database.')

def setup(bot):
    bot.add_cog(Mgmt())
