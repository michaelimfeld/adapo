"""
    Provides a YAML configuration file reader.
"""

import yaml
from adapo.logger import Logger


class Config(object):
    """
        YAML configuration file reader.
    """

    def __init__(self, path):
        self._cfg = None
        self._log = Logger()
        self._path = path
        self.load_config()

    def load_config(self):
        """
            Loads config file.
        """
        config_file = open(self._path, "r")
        self._cfg = yaml.load(config_file)
        config_file.close()
        self._log.info("config file '%s' loaded" % self._path)

    def __getattr__(self, attr):
        """
            Returns configuration value by attribute.
        """
        value = self._cfg.get(attr)
        if not value:
            self._log.warn(
                "could not find value for key '{0}' in '{1}'"
                .format(attr, self._path)
            )
        return value
