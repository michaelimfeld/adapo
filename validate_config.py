#!/usr/bin/python
import yaml
import urllib2
import re
from logger import Logger

class ConfigValidator(object):

    def __init__(self, cfg_file="csgo.conf"):
        # load config file
        config_file = open(cfg_file, "r")
        self._config_yaml = yaml.load(config_file)
        config_file.close()

        self._log = Logger()

        self._fastdl_url = self._config_yaml["csgo"]["fast_dl_server"]
        self._maps = self._config_yaml["csgo"]["maps"]


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
            self._log.error("fastdl server '%s' unreachable" % self._fastdl_url)
            return False

        # get all present maps from fastdl_url
        maps_present = []
        for map_url in re.findall(pattern, response):
            if 'bz2' in map_url:
                map_name = map_url.split(".")[0]
                maps_present.append(map_name)

        for map in self._maps:
            if map not in maps_present:
                self._log.error("map '%s' not available on fastdl server" % map)
                continue
            self._log.success("map '%s' found on fastdl server" % map)

def main():
    ConfigValidator().validate_maps()

if __name__ == "__main__":
    main()
