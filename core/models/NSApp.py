from . import Model
from peewee import CharField, FixedCharField

class NSApp(Model):
    name = CharField()
    author = CharField()
    website_url = CharField(null = True)
    source_code_url = CharField(null = True)
    token = FixedCharField(null = True, unique = True, length = 32)
