import os
from subprocess import Popen, PIPE, STDOUT
from logger import Logger
from configvalidator import ConfigValidator
from serverconfig import ServerConfig


class CSGOServer(object):
    """
        CS:GO Server Installer
    """

    STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
    LOG_FILE = "install.log"

    def __init__(self):
        self._logger = Logger()
        self._steamcmd_path = os.path.join(os.path.os.getcwd(), "steamcmd")
        self._config = ServerConfig()

    def install(self):
        """
            install csgo server
        """
        if not self.install_steamcmd():
            self._logger.error("steamcmd installation failed!")
            return False
        if not self.install_csgo():
            self._logger.error("csgo installation failed, check '%s' for errors!" % self.LOG_FILE)
            return False

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
        root_dir = self._config.get("csgo.root_directory")

        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        ret = self.open_subprocess(
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

        if ret:
            self._logger.info("csgo server successfully installed")

        return ret

    def download_steamcmd(self):
        """
            downloads steamcmd.tar.gz
        """
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
        path = os.path.join(self._steamcmd_path, "steamcmd_linux.tar.gz")

        return self.open_subprocess(
            [
                "tar",
                "-xvzf",
                path
            ],
            self._steamcmd_path
        )

    def clean_steamcmd(self):
        """
            clean steamcmd directory
        """
        path = os.path.join(self._steamcmd_path, "steamcmd_linux.tar.gz")

        if os.path.exists(path):
            os.remove(path)

        return True

    def install_steamcmd(self):
        """
            installs steamcmd
        """
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

        if not self.unpack_steamcmd():
            self._logger.error("could not unpack steamcmd!")
            return False

        if not self.clean_steamcmd():
            self._logger.error("could not clean steamcmd!")
            return False

        self._logger.info("steamcmd successfully installed")
        return True


def main():
    """
        main
    """
    CSGOServer().install()

if __name__ == "__main__":
    main()
