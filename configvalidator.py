#!/usr/bin/python
import yaml
import urllib2
import re
from logger import Logger
from serverconfig import ServerConfig

class ConfigValidator(object):

    def __init__(self, cfg_file="csgo.conf"):
        self._logger= Logger()
        self._config = ServerConfig()

        self._fastdl_url = self._config.get("csgo.fastdl_server")
        self._maps = self._config.get("csgo.maps")

        self._logger.info("csgo config file validation initialized")

    def validate(self):
        """
            validate csgo config
        """
        self._logger.info("validating maps ...")
        maps = self.validate_maps()
        # implement plugin validation
        plugins = True

        if not (maps or plugins):
            return False


    def validate_maps(self):
        """
            check if all listed maps are
            available on the fastdl server
        """
        maps_url = "%s/maps/" % self._fastdl_url

        pattern = r'href=[\'"]?([^\'" >]+)'

        response = None
        try:
            response = urllib2.urlopen(maps_url).read()
        except urllib2.URLError:
            self._logger.error("fastdl server '%s' unreachable" % self._fastdl_url)
            return False

        # get all present maps from fastdl_url
        maps_present = []
        for map_url in re.findall(pattern, response):
            if 'bz2' in map_url:
                map_name = map_url.split(".")[0]
                maps_present.append(map_name)

        for map in self._maps:
            if map not in maps_present:
                self._logger.error("map '%s' not available on fastdl server" % map)
                return False
                continue
            self._logger.info("map '%s' found on fastdl server" % map)

def main():
    ConfigValidator().validate()

if __name__ == "__main__":
    main()
