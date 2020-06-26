from os import getenv
from peewee import PostgresqlDatabase
from .Bot import Bot

db = PostgresqlDatabase(
    getenv('PSQL_DATABASE'),
    host = getenv('PSQL_HOST'),
    port = getenv('PSQL_PORT'),
    user = getenv('PSQL_USER'),
    password = getenv('PSQL_PASSWORD'),
    autoconnect = False
)

db.connect()

bot = Bot()
