#!/usr/bin/python
import os
import shutil
from logger import Logger

class Initializer(object):

    DATA_DIR = "/usr/share/adapo/data"

    def __init__(self):
        self._logger = Logger()

    def init(self, args):
        """
            create installer directory in cwd
        """
        installer_dir = os.path.join(os.path.os.getcwd(), "adapo-installer")
        if os.path.exists(installer_dir):
            self._logger.error("installer dir: '%s' already exists" % installer_dir)
            exit(1)

        os.makedirs(installer_dir)

        # copy example config file to installer dir
        src = os.path.join(self.DATA_DIR, "csgo.conf")
        dst = installer_dir
        shutil.copy2(src, dst)



