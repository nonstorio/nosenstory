from .Model import Model
from .NsPlayer import NsPlayer
from .NsGuild import NsGuild
from .NsChannel import NsChannel

models = [
    NsPlayer,
    NsGuild,
    NsChannel
]

def setup(_):
    for model in models:
        model.create_table()
