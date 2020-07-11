import peewee

class DatabaseProxy(peewee.DatabaseProxy):
    def initialize(self, obj, models = [], drop = False, create = True):
        super().initialize(obj)
        if not obj: return
        if drop:
            self.drop_tables(models)
        if create:
            self.create_tables(models)
