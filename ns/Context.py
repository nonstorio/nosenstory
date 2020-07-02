from discord.ext import commands

class Context(commands.Context):
    async def reply(self, content = None, **kwargs):
        mention = f'<@{self.author.id}>'
        return await self.send(f'{mention} ⦗ {content} ⦘' if content else mention, **kwargs)
    async def edit_reply(self, message, content = None, **kwargs):
        mention = f'<@{self.author.id}>'
        return await message.edit(content = f'{mention} ⦗ {content} ⦘' if content else mention, **kwargs)
    async def sendToMgmt(self, content = None, ping = False, **kwargs):
        from ns.models import NsChannel, NsMgmt
        query = (NsMgmt
            .select()
            .join(NsChannel)
            .where(
                NsMgmt.user.is_null(),
                NsMgmt.channel.is_null(False)
            ))
        for nsmgmt in query:
            await (self.bot
                .get_channel(nsmgmt.channel.ref_id)
                .send(content, **kwargs))
        return True
