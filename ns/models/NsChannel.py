from . import Model, NsGuild
from peewee import BigIntegerField, CharField, ForeignKeyField, IntegerField

class NsChannel(Model):
    ref_id = BigIntegerField(unique = True)
    ref_name = CharField()
    guild = ForeignKeyField(NsGuild)
    lang = CharField(max_length = 3, null = True)
    rounds_held = IntegerField(default = 0)

    class Meta:
        indexes = (
            (('ref_id', 'ref_name'), True),
        )
