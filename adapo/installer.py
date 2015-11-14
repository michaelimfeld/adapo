import os
import shutil
from subprocess import Popen, PIPE, STDOUT
from logger import Logger
from configvalidator import ConfigValidator
from serverconfig import ServerConfig


class Installer(object):
    """
        CS:GO Server Installer
    """

    STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
    LOG_FILE = "/tmp/adapo_installer.log"
    STEAMCMD_TAR = "steamcmd_linux.tar.gz"
    DATA_DIR = "/usr/share/adapo/data"

    def __init__(self):
        self._logger = Logger()
        self._steamcmd_path = os.path.join(os.path.os.getcwd(), "steamcmd")
        self._config = ServerConfig()

    def install(self, args):
        """
            install csgo server
        """
        if not self.install_steamcmd():
            self._logger.error("steamcmd installation failed!")
            return False
        self._logger.info("steamcmd successfully installed")

        if not self.install_csgo():
            self._logger.error("csgo installation failed, check '%s' for errors!" % self.LOG_FILE)
            return False
        self._logger.info("csgo successfully installed")

        if not self.install_plugins():
            self._logger.error("plugin installation failed, check '%s' for errors!" % self.LOG_FILE)
            return False
        self._logger.info("plugins successfully installed")

        return True

    def uninstall(self):
        """
            uninstall csgo server
        """
        #FIXME: implement uninstall
        self._logger.info("uninstall not implemented yet")

    def open_subprocess(self, args, cwd):
        """
            open sub process
            pipe stdout and stderr to log file
        """
        proc = Popen(
            args,
            cwd=self._steamcmd_path,
            stdout=PIPE,
            stderr=PIPE
        )

        #FIXME: use logger class
        log_file = open(self.LOG_FILE, "a")
        for line in iter(proc.stdout.readline, ""):
            log_file.write(line)
            log_file.flush()

        log_file.close()
        proc.stdout.close()

        ret = proc.wait()

        if ret != 0:
            return False
        return True


    def install_csgo(self):
        """
            install csgo server
            steamcmd:
                ./steamcmd.sh +login anonymous +force_install_dir /home/steam/server/csgo/ +app_update 740 +quit
        """
        self._logger.info("installing csgo with steamcmd ...")
        root_dir = self._config.get("csgo.root_directory")

        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        return self.open_subprocess(
            [
                "./steamcmd.sh",
                "+login",
                "anonymous",
                "+force_install_dir",
                root_dir,
                "+app_update",
                "740",
                "+quit"
            ],
            self._steamcmd_path
        )

    def download_steamcmd(self):
        """
            downloads steamcmd.tar.gz
        """
        self._logger.info("downloading steamcmd ...")
        return self.open_subprocess(
            [
                "wget",
                self.STEAMCMD_URL
            ],
            self._steamcmd_path
        )

    def unpack_steamcmd(self):
        """
            unpack steamcmd.tar.gz
        """
        self._logger.info("unpacking steamcmd ...")
        path = os.path.join(self._steamcmd_path, self.STEAMCMD_TAR)

        return self.open_subprocess(
            [
                "tar",
                "-xvzf",
                self.STEAMCMD_TAR
            ],
            self._steamcmd_path
        )

    def clean_steamcmd(self):
        """
            clean steamcmd directory
        """
        self._logger.info("cleaning up steamcmd directory ...")
        path = os.path.join(self._steamcmd_path, self.STEAMCMD_TAR)

        if os.path.exists(path):
            os.remove(path)

        return True

    def install_steamcmd(self):
        """
            installs steamcmd
        """
        self._logger.info("installing steamcmd ...")
        if not os.path.exists(self._steamcmd_path):
            os.makedirs(self._steamcmd_path)

        steamcmd_tar = os.path.join(
            self._steamcmd_path,
            "steamcmd_linux.tar.gz"
        )

        if os.path.exists(steamcmd_tar):
            self._logger.error("steamcmd_linux.tar.gz already exists!")
            return False

        if not self.download_steamcmd():
            self._logger.error("could not download steamcmd!")
            return False
        self._logger.info("steamcmd successfully downloaded")

        if not self.unpack_steamcmd():
            self._logger.error("could not unpack steamcmd!")
            return False
        self._logger.info("steamcmd successfully unpacked")

        if not self.clean_steamcmd():
            self._logger.error("could not clean steamcmd!")
            return False
        self._logger.info("steamcmd successfully cleaned")

        return True

    def create_start_script(self):
        """
            create start.sh script in csgo root dir
        """
        #FIXME: implement start script creation
        #example:
        #./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 0 +map am_must2 -tickrate 128 -maxplayers_override 32 -condebug

    def install_plugins(self):
        """
            install sourcemod plugins
        """
        self._logger.info("installing plugins ...")

        self._logger.info("simple plugins successfully installed")
        return True



def main():
    """
        main
    """
    Installer().install()

if __name__ == "__main__":
    main()
