import peewee as pw
from core.NsDatabase import NsDatabase

db = NsDatabase()

class Model(pw.Model):
    class Meta:
        database = db
        legacy_table_names = False
