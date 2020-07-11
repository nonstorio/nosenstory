import peewee as pw
from core.DatabaseProxy import DatabaseProxy

db = DatabaseProxy()

class Model(pw.Model):
    class Meta:
        database = db
        legacy_table_names = False
