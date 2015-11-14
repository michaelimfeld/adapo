#!/usr/bin/python
import yaml
from logger import Logger


class ServerConfig(object):
    """
        csgo server configuration
    """

    CONFIG_FILE = "csgo.conf"

    def __init__(self):
        self._config = None
        self._logger = Logger()
        self.load_config()

    def load_config(self):
        """
            load config file
        """
        config_file = open(self.CONFIG_FILE, "r")
        self._config = yaml.load(config_file)
        config_file.close()
        self._logger.info("config file '%s' loaded" % self.CONFIG_FILE)

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
        #FIXME: try, except KeyError

        keys = key.split(".")
        value = self._config[keys[0]]

        for key in keys[1:]:
            value = value[key]

        return value
