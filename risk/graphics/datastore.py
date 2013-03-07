import sets

import risk

class Datastore(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not Datastore._instance:
            Datastore._instance = super(Datastore, cls).__new__(Datastore,
                    *args, **kwargs)
            Datastore._instance.datastore = {'DEFAULT': {}}
        return Datastore._instance

    def add_entry(self, key, value, storage='DEFAULT'):
        if not self.datastore.has_key(storage):
            self.datastore[storage] = {}
        self.datastore[storage][key] = value

    def get_entry(self, key, storage='DEFAULT'):
        return self.datastore[storage][key]
    
    def get_storage(self, storage='DEFAULT'):
        return self.datastore[storage]

    def has_entry(self, key, storage='DEFAULT'):
        try:
            return self.datastore[storage].has_key(key)
        except KeyError:
            return False

Datastore.instance = None
