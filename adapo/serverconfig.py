#!/usr/bin/python
import yaml
from logger import Logger


class ServerConfig(object):
    """
        csgo server configuration
    """

    def __init__(self, path):
        self._config = None
        self._logger = Logger()
        self._path = path
        self.load_config()

    def load_config(self):
        """
            load config file
        """
        config_file = open(self._path, "r")
        self._config = yaml.load(config_file)
        config_file.close()
        self._logger.info("config file '%s' loaded" % self._path)

    def get(self, key):
        """
            get config value by key
            examples:
            |---------------|-----------------------------|
            | input key     | output value                |
            |---------------|-----------------------------|
            | csgo.maps     | ['de_dust2', 'de_mirage']   |
            | server_name   | 'My Counter-Strike Server'  |
            |---------------|-----------------------------|
        """
        try:
            keys = key.split(".")
            value = self._config[keys[0]]

            for key in keys[1:]:
                value = value[key]

            return value

        except KeyError:
            self._logger.error(
                "could not find key '%s' in '%s'" % (key, self_path)
            )
            return False
