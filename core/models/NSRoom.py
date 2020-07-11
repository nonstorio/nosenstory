from . import Model, NSLobby, NSHome
from peewee import BigIntegerField, CharField, ForeignKeyField

class NSRoom(Model):
    lobby = ForeignKeyField(NSLobby, backref = 'rooms')
    home = ForeignKeyField(NSHome, backref = 'rooms')
    id_int = BigIntegerField(null = True)
    id_str = CharField(null = True)

NSRoom.add_index(
    NSRoom.home,
    NSRoom.id_int,
    unique = True
)
NSRoom.add_index(
    NSRoom.home,
    NSRoom.id_str,
    unique = True
)
