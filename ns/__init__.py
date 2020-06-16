import os
from peewee import PostgresqlDatabase
from .Bot import Bot

db = PostgresqlDatabase(
    os.getenv('PSQL_DATABASE'),
    host = os.getenv('PSQL_HOST'),
    port = os.getenv('PSQL_PORT'),
    user = os.getenv('PSQL_USER'),
    password = os.getenv('PSQL_PASSWORD'),
    autoconnect = False
)

db.connect()

bot = Bot()
