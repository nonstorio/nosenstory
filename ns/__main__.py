import dotenv
import logging
from core import db, models
from ns.Bot import Bot
from os import getenv
from peewee import PostgresqlDatabase


dotenv.load_dotenv(dotenv_path = '../.env')
logging.basicConfig(level = logging.INFO)

db.initialize(
    PostgresqlDatabase(
        getenv('PSQL_DATABASE'),
        host = getenv('PSQL_HOST'),
        port = getenv('PSQL_PORT'),
        user = getenv('PSQL_USER'),
        password = getenv('PSQL_PASSWORD')
    ),
    models = models
)

Bot()
