from . import Model, NSUser, NSHome, NSLobby
from peewee import ForeignKeyField

class NSMgmt(Model):
    user = ForeignKeyField(NSUser, null = True)
    home = ForeignKeyField(NSHome, null = True)
    lobby = ForeignKeyField(NSLobby, null = True)

NSMgmt.add_index(
    NSMgmt.user,
    NSMgmt.home,
    unique = True
)
NSMgmt.add_index(
    NSMgmt.user,
    NSMgmt.lobby,
    unique = True
)
