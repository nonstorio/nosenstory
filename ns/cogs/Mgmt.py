from core.const import COLOUR, EMOJI, MISC
from core.models import (
    NsChannel,
    NsGuild,
    NsMgmt,
    NsUser
)
from discord import Embed, TextChannel
from discord.ext.commands import (
    CheckFailure,
    Cog,
    UserInputError,
    check,
    group,
    guild_only
)
from ns import Context
from typing import Optional


async def mgmt_guild(ctx: Context):
    if ctx.author.permissions_in(ctx.channel).administrator:
        return True
    nsmgmt = (NsMgmt
        .select()
        .join_from(NsMgmt, NsUser)
        .join_from(NsMgmt, NsGuild)
        .where(
            NsUser.ref_id == ctx.author.id,
            NsGuild.ref_id == ctx.guild.id
        )
    ).count()
    if nsmgmt == 0:
        raise CheckFailure(f'You do not have NS Management permissions for guild.')
    return True

async def mgmt_channel(ctx: Context):
    if ctx.author.permissions_in(ctx.channel).administrator:
        return True
    nsmgmt = (NsMgmt
        .select()
        .join_from(NsMgmt, NsUser)
        .join_from(NsMgmt, NsGuild)
        .join_from(NsMgmt, NsChannel)
        .where(
            NsUser.ref_id == ctx.author.id,
            (NsGuild.ref_id == ctx.guild.id) |
            (NsChannel.ref_id == ctx.channel.id)
        )
    ).count()
    if nsmgmt == 0:
        raise CheckFailure(f'You do not have NS Management permissions for channel or guild.')
    return True


class Mgmt(Cog, name = 'NS Management'):
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

    @channel.command(aliases = ['add', 'register'])
    @check(mgmt_guild)
    async def assign(self, ctx, channel: Optional[TextChannel]):
        '''Assign bot to a channel, so game can be run there.'''
        channel = channel or ctx.message.channel
        nsguild = NsGuild.get(NsGuild.ref_id == ctx.guild.id)
        _, new = NsChannel.get_or_create(
            ref_id = channel.id,
            ref_name = channel.name,
            guild = nsguild
        )
        if new:
            await ctx.reply(f'I am now assigned to <#{channel.id}>. Happy play!')
        else:
            await ctx.reply(f'Channel <#{channel.id}> is already in my database.')

    @channel.command(aliases = ['hub', 'nsm', 'mgt', 'mngt', 'mngmt', 'management'])
    @check(mgmt_guild)
    async def mgmt(self, ctx, channel: Optional[TextChannel]):
        '''Mark a channel as NS Management notifications hub of guild.'''
        channel = channel or ctx.message.channel
        nsguild = NsGuild.get(NsGuild.ref_id == ctx.guild.id)
        nschannel, _ = NsChannel.get_or_create(
            ref_id = channel.id,
            ref_name = channel.name,
            guild = nsguild
        )
        nsmgmt, _ = NsMgmt.get_or_create(
            guild = nsguild
        )
        nsmgmt.channel = nschannel
        nsmgmt.save()
        await ctx.reply(f'Marked <#{channel.id}> as NS Management notifications hub of guild.')

    @channel.command(aliases = ['kill', 'remove', 'delete', 'destroy'])
    @check(mgmt_guild)
    async def resign(self, ctx, channel: Optional[TextChannel]):
        '''Remove all data related to channel.'''
        channel = channel or ctx.message.channel
        nschannel = NsChannel.get_or_none(NsChannel.ref_id == channel.id)
        if not nschannel:
            return await ctx.reply(f'Channel <#{channel.id}> was not registered in my database.')
        prompt = await ctx.reply(f'Game data related to <#{channel.id}> will be deleted. React with `{EMOJI.YES}`, **if you are sure**.')
        await prompt.add_reaction(EMOJI.YES)
        try:
            await ctx.bot.wait_for(
                'reaction_add',
                timeout = 10.0,
                check = lambda reaction, user: reaction.emoji == EMOJI.YES and user.id == ctx.author.id and reaction.message.id == prompt.id
            )
            nschannel.delete_instance(recursive = True)
            await ctx.edit_reply(prompt, content = f'Game data related to <#{channel.id}> was deleted.')
        except: pass
        await prompt.clear_reactions()


def setup(bot):
    bot.add_cog(Mgmt())
