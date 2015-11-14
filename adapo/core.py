#!/usr/bin/python
import os
from argparse import ArgumentParser
from initializer import Initializer
from configvalidator import ConfigValidator
from installer import Installer

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    arg_init = subparsers.add_parser("init", help="Create installer directory.")
    arg_init.set_defaults(func=Initializer().init)

    arg_validate = subparsers.add_parser("validate", help="Validate configuration file 'csgo.conf'.")
    arg_install = subparsers.add_parser("install", help="Install CS:GO Server with configuration file 'csgo.conf'.")

    if os.path.exists("csgo.conf"):
        arg_validate.set_defaults(func=ConfigValidator().validate)
        #FIXME: add config file path param
        arg_install.set_defaults(func=Installer().install)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
