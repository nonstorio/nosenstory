from . import Model
from peewee import CharField, IntegerField

class NSLobby(Model):
    name = CharField(null = True)
    lang = CharField(null = True)
    rounds_held = IntegerField(default = 0)
