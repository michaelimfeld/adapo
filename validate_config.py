#!/usr/bin/python
import yaml
import urllib2
import re
from logger import Logger

def validate_maps(maps, fastdl_url):
    """
        check if all listed maps are
        available on the fastdl server
    """
    maps_url = "%s/maps/" % fastdl_url

    pattern = r'href=[\'"]?([^\'" >]+)'
    response = urllib2.urlopen(maps_url).read()

    # get all present maps from fastdl_url
    maps_present = []
    for map_url in re.findall(pattern, response):
        if 'bz2' in map_url:
            map_name = map_url.split(".")[0]
            maps_present.append(map_name)

    for map in maps:
        if map not in maps_present:
            Logger().error("map not available on fastdl server: '%s'" % map)

def main():
    with open("csgo.conf", "r") as config_file:
        config_yaml = yaml.load(config_file)

        fastdl_url = config_yaml["csgo"]["fast_dl_server"]
        maps = config_yaml["csgo"]["maps"]

        validate_maps(maps, fastdl_url)

if __name__ == "__main__":
    main()
