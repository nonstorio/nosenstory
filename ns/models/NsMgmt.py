from . import Model, NsUser, NsGuild, NsChannel
from peewee import ForeignKeyField

class NsMgmt(Model):
    user = ForeignKeyField(NsUser, null = True)
    guild = ForeignKeyField(NsGuild, null = True)
    channel = ForeignKeyField(NsChannel, null = True)

NsMgmt.add_index(NsMgmt.user, NsMgmt.guild, unique = True)
NsMgmt.add_index(NsMgmt.user, NsMgmt.channel, unique = True)
