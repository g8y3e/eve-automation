import json
from singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        self._config_path = './config/config.json'
        self._data = json.load(open(self._config_path))

    def get(self):
        return self._data

    def save(self):
        with open(self._config_path, 'w') as outfile:
            json.dump(self._data, outfile, indent=4)


config = Config().get()
config_save = Config().save



