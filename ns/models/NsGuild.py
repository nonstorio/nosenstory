from . import Model
from peewee import BigIntegerField, CharField, FixedCharField

class NsGuild(Model):
    ref_id = BigIntegerField(unique = True)
    lang = CharField(null = True)
    prefix = FixedCharField(max_length = 1, null = True)
