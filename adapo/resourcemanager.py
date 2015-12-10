"""
    ResourceManager
"""

import os
import subprocess
from adapo.logger import Logger


class ResourceManager(object):
    """
        Provides generic resource functions
    """

    LOG_FILE = "/tmp/adapo_installer.log"

    def __init__(self):
        self._logger = Logger()

    def open_subprocess(self, args, cwd):
        """
            open sub process
            pipe stdout and stderr to log file
        """
        proc = subprocess.Popen(
            ["stdbuf", "-oL"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            close_fds=True
        )

        # FIXME: Use logger class
        log_file = open(self.LOG_FILE, "a")
        for line in iter(proc.stdout.readline, b""):
            log_file.write(line)
            log_file.flush()

        for line in iter(proc.stderr.readline, b""):
            log_file.write(line)
            log_file.flush()

        log_file.close()
        proc.stdout.close()
        ret = proc.wait()

        if ret != 0:
            return False
        return True

    def download(self, url, dst):
        """
            download file from url to given
            destination directory
        """
        self._logger.info("downloading '%s' ..." % url)
        os.chdir(dst)

        # remove file with same name, if exists
        filename = url.split("/")[-1]
        if os.path.exists(os.path.join(dst, filename)):
            self._logger.info("removing existing file '%s' ..." % filename)
            os.remove(os.path.join(dst, filename))

        ret = subprocess.call(
            [
                "wget",
                url
            ]
        )

        if ret != 0:
            return False

        return True

    def unpack(self, path, cwd):
        """
            unpack tar.gz file
        """
        self._logger.info("unpacking '%s' ..." % path)

        return self.open_subprocess(
            [
                "tar",
                "-xvzf",
                path
            ],
            cwd
        )

    def copy_tree(self, src, dst):
        """
            copy all files in src directory
            to dst --> cp -r src/* dst/
        """
        if not src.endswith("/"):
            src += "/"

        src += "*"
        cmd = "cp -r %s %s" % (src, dst)

        proc = subprocess.Popen(
            cmd,
            shell="true"
        )
        ret = proc.wait()

        if ret != 0:
            return False

        return True
