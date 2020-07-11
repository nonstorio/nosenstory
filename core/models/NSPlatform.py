from . import Model
from peewee import FixedCharField, CharField

class NSPlatform(Model):
    token = FixedCharField(unique = True, length = 32)
    name = CharField()
