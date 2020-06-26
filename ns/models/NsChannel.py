from . import Model, NsGuild
from peewee import BigIntegerField, CharField, BooleanField, ForeignKeyField, IntegerField

class NsChannel(Model):
    ref_id = BigIntegerField(unique = True)
    ref_name = CharField()
    guild = ForeignKeyField(NsGuild)
    mgmt = BooleanField(default = False)
    lang = CharField(null = True)
    rounds_held = IntegerField(default = 0)

NsChannel.add_index(NsChannel.ref_name, NsChannel.guild, unique = True)
NsChannel.add_index(NsChannel.ref_name, NsChannel.guild, unique = True)
NsChannel.add_index(NsChannel.guild, NsChannel.mgmt, unique = True, where = (NsChannel.mgmt == True))
