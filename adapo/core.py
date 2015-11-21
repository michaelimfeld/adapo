#!/usr/bin/python
"""
    Adapo Core Application
"""

import os
from argparse import ArgumentParser
from adapo.configvalidator import ConfigValidator
from adapo.installer import Installer
from adapo.logger import Logger


class AdapoCore(object):
    """
        Provides helper functions to trigger
        installer functions per config file
    """

    CONFIG_PATH = "/etc/adapo/servers.d/"

    def __init__(self):
        self._logger = Logger()
        self._configs = []
        self.get_configs()

    def install(self, _):
        """
            trigger installer for every
            loaded config file
        """
        for config in self._configs:
            Installer(config).install()

    def validate(self, _):
        """
            trigger validator for every
            loaded config file
        """
        for config in self._configs:
            if ConfigValidator(config).validate():
                self._logger.info("config file '%s'is valid" % config)
                continue
            self._logger.error("config file '%s'is invalid!" % config)

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
    """
        Parse arguments
    """

    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    arg_install = subparsers.add_parser(
        "install",
        help="Install all servers configured in '/etc/adapo/servers.d/*.cfg'"
    )
    arg_validate = subparsers.add_parser(
        "validate",
        help="Validate all servers configured in '/etc/adapo/servers.d/*.cfg'"
    )

    arg_install.set_defaults(func=AdapoCore().install)
    arg_validate.set_defaults(func=AdapoCore().validate)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
