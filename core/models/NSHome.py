from . import Model, NSApp
from peewee import ForeignKeyField, BigIntegerField, CharField, FixedCharField

class NSHome(Model):
    app = ForeignKeyField(NSApp, backref = 'homes')
    id_int = BigIntegerField(null = True)
    id_str = CharField(null = True)
    lang = CharField(null = True)
    prefix = FixedCharField(max_length = 1, null = True)

NSHome.add_index(
    NSHome.app,
    NSHome.id_int,
    unique = True,
    where = (NSHome.id_int.is_null(False))
)
NSHome.add_index(
    NSHome.app,
    NSHome.id_str,
    unique = True,
    where = (NSHome.id_str.is_null(False))
)
