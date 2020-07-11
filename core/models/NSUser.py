from . import Model, NSHome
from peewee import ForeignKeyField, BigIntegerField, CharField, IntegerField

class NSUser(Model):
    origin = ForeignKeyField('self', null = True, backref = 'linked_users')
    home = ForeignKeyField(NSHome, backref = 'users')
    id_int = BigIntegerField(null = True)
    id_str = CharField(null = True)
    rounds_played = IntegerField(default = 0)

NSUser.add_index(
    NSUser.origin,
    NSUser.home,
    unique = True,
    where = (NSUser.origin.is_null(False))
)
NSUser.add_index(
    NSUser.home,
    NSUser.id_int,
    unique = True,
    where = (NSUser.id_int.is_null(False))
)
NSUser.add_index(
    NSUser.home,
    NSUser.id_str,
    unique = True,
    where = (NSUser.id_str.is_null(False))
)
