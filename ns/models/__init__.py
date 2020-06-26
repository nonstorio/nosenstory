from ns import db
from .Model import Model
from .NsUser import NsUser
from .NsGuild import NsGuild
from .NsChannel import NsChannel
from .NsMgmt import NsMgmt

models = [
    NsUser,
    NsGuild,
    NsChannel,
    NsMgmt
]

if input('Would you like to drop tables before start? (y/N) ').lower() == 'y':
    db.drop_tables(models)

def setup(_):
    for model in models:
        model.create_table()
