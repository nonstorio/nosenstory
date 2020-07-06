from core.models import (
    NsGuild,
    NsChannel,
    NsMgmt
)
from discord.ext import commands


class Context(commands.Context):
    async def reply(self, content = None, **kwargs):
        mention = f'<@{self.author.id}>'
        return await self.send(f'{mention} ⦗ {content} ⦘' if content else mention, **kwargs)

    async def edit_reply(self, message, content = None, **kwargs):
        mention = f'<@{self.author.id}>'
        return await message.edit(content = f'{mention} ⦗ {content} ⦘' if content else mention, **kwargs)

    async def send_to_mgmt(self, content = None, ping = False, **kwargs):
        query = (NsMgmt
            .select()
            .join_from(NsMgmt, NsGuild)
            .join_from(NsMgmt, NsChannel)
            .where(
                NsMgmt.user.is_null(),
                NsMgmt.guild.ref_id == self.guild.id,
                NsMgmt.channel.is_null(False)
            ))
        for nsmgmt in query:
            await (self.bot
                .get_channel(nsmgmt.channel.ref_id)
                .send(content, **kwargs))
        return True
