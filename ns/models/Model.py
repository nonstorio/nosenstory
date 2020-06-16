import peewee
from ns import db

class Model(peewee.Model):
    class Meta:
        database = db
        legacy_table_names = False
