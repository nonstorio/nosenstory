from discord.ext import commands

class Context(commands.Context):
    async def reply(self, content = None, **kwargs):
        mention = f'<@{self.author.id}>'
        return await self.send(f'{mention} ⦗ {content} ⦘' if content else mention, **kwargs)
