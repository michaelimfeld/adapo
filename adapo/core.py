#!/usr/bin/python
import os
from argparse import ArgumentParser
from initializer import Initializer
from configvalidator import ConfigValidator
from installer import Installer
from logger import Logger


class AdapoCore(object):

    CONFIG_PATH = "/etc/adapo/servers.d/"

    def __init__(self):
        self._logger = Logger()
        self._configs = []
        self.get_configs()

    def install(self, args=None):
        """
            trigger installer for every
            loaded config file
        """
        for config in self._configs:
            Installer(config).install()

    def get_configs(self):
        """
            add all config files in
            /etc/adapo/servers.d/
            to list
        """
        self._logger.info("loading server configuration files ...")
        for config in os.listdir(self.CONFIG_PATH):
            if config.endswith(".cfg") and config != "example.cfg":
                self._configs.append(os.path.join(self.CONFIG_PATH, config))


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    arg_install = subparsers.add_parser(
        "install",
        help="Install all servers configured in '/etc/adapo/servers.d/*.cfg'"
    )
    arg_install.set_defaults(func=AdapoCore().install)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
