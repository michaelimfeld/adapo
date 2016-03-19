"""
    Configuration Validator
"""

import re
import os
import urllib2
from adapo.logger import Logger
from adapo.config import Config


class ConfigValidator(object):
    """
        Configuration Validator
    """

    ADAPO_CONF = "/etc/adapo/main.cfg"

    def __init__(self, config_path):
        self._log = Logger()

        # load global adapo configuration
        self._adapo_config = Config(self.ADAPO_CONF)
        self._data_path = self._adapo_config.get("data_src_path")

        self._config = Config(config_path)
        self._root_dir = self._config.get("csgo.root_directory")
        self._fastdl_url = self._config.get("server_config.sv_downloadurl")
        self._maps = self._config.get("csgo.maps")
        self._plugins = self._config.get("sourcemod.plugins")

        self._log.info("csgo config file validation initialized")

    def validate(self):
        """
            validate csgo config
        """
        if not self.validate_maps():
            return False
        if not self.validate_plugins():
            return False

        return True

    def validate_plugins(self):
        """
            check if all listed plugins are
            available in data/plugins directory
        """
        self._log.info("validating plugins ...")

        for plugin in self._plugins:
            path = os.path.join(self._data_path, "plugins", plugin)

            if os.path.exists("%s.smx" % path):
                self._log.info("found simple plugin '%s.smx'" % path)
                continue

            if os.path.isdir(path):
                self._log.info("found complex plugin '%s'" % path)
                continue

            self._log.error("could not find plugin '%s(.smx)'!" % path)
            return False

        return True

    def validate_maps(self):
        """
            check if all listed maps are
            available on the fastdl server
        """
        self._log.info("validating maps ...")

        maps_url = "%s/maps/" % self._fastdl_url
        pattern = r'href=[\'"]?([^\'" >]+)'
        response = None

        try:
            response = urllib2.urlopen(maps_url).read()
        except urllib2.URLError:
            self._log.error(
                "fastdl server '%s' unreachable" % self._fastdl_url
            )
            return False

        # get all present maps from fastdl_url
        maps_present = []
        for map_url in re.findall(pattern, response):
            if 'bz2' in map_url:
                map_name = map_url.split(".")[0]
                maps_present.append(map_name)

        for _map in self._maps:
            if _map not in maps_present:
                self._log.error(
                    "map '%s' not available on fastdl server" % _map
                )
                return False
            self._log.info("map '%s' found on fastdl server" % _map)
