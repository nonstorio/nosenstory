from . import Model
from peewee import BigIntegerField, IntegerField

class NsUser(Model):
    ref_id = BigIntegerField(unique = True)
    rounds_played = IntegerField(default = 0)
