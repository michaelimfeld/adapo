import os
import stat
import shutil
import subprocess
from logger import Logger
from serverconfig import ServerConfig
from parameters import Parameters


class Installer(object):
    """
        CS:GO Server Installer
    """

    LOG_FILE = "/tmp/adapo_installer.log"
    ADAPO_CONF = "/etc/adapo/main.cfg"

    def __init__(self, config_path):
        self._logger = Logger()

        # load global adapo configuration
        self._adapo_config = ServerConfig(self.ADAPO_CONF)
        self._steamcmd_path = self._adapo_config.get("steamcmd_path")
        self._steamcmd_url = self._adapo_config.get("steamcmd_dl_url")
        self._metamod_url = self._adapo_config.get("metamod_dl_url")
        self._sourcemod_url = self._adapo_config.get("sourcemod_dl_url")
        self._data_path = self._adapo_config.get("data_src_path")

        # load specific cs:go server configuration
        self._config = ServerConfig(config_path)
        self._root_dir = self._config.get("csgo.root_directory")

    def install(self):
        """
            install csgo server
        """
        if not self.install_steamcmd():
            self._logger.error(
                "steamcmd installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("steamcmd successfully installed")

        if not self.install_csgo():
            self._logger.error(
                "csgo installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("csgo successfully installed")

        if not self.install_metamod():
            self._logger.error(
                "metamod installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("metamod successfully installed")

        if not self.install_sourcemod():
            self._logger.error(
                "sourcemod installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("sourcmod successfully installed")

        if not self.install_plugins():
            self._logger.error(
                "plugin installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("plugins successfully installed")

        if not self.install_maps():
            self._logger.error(
                "map installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("maps successfully installed")

        if not self.write_server_config():
            self._logger.error(
                "could not install config!, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._logger.info("server config successfully installed")

        if not self.create_start_script():
            self._logger.error(
                "could not create start script!, "
                "check '%s' for errors!" % self.LOG_FILE
            )
        self._logger.info("start script successfully written")

        return True

    def uninstall(self):
        """
            uninstall csgo server
        """
        # FIXME: Implement uninstall
        self._logger.info("uninstall not implemented yet")

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

    def install_csgo(self):
        """
            install csgo server
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

    def download(self, url, dst):
        """
            download file from url to given
            destination directory
        """
        self._logger.info("downloading '%s' ..." % url)
        os.chdir(dst)
        ret = subprocess.call(
            [
                "wget",
                url
            ]
        )

        if ret != 0:
            return False

        return True

    def download_steamcmd(self):
        """
            download steamcmd.tar.gz
        """
        self._logger.info("downloading steamcmd ...")
        return self.download(self._steamcmd_url, self._steamcmd_path)

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

    def unpack_steamcmd(self):
        """
            unpack steamcmd.tar.gz
        """
        self._logger.info("unpacking steamcmd ...")

        steamcmd_tar = self._steamcmd_url.split("/")[-1]
        return self.unpack(steamcmd_tar, self._steamcmd_path)

    def clean_steamcmd(self):
        """
            clean steamcmd directory
        """
        self._logger.info("cleaning up steamcmd directory ...")

        steamcmd_tar = self._steamcmd_url.split("/")[-1]
        path = os.path.join(self._steamcmd_path, steamcmd_tar)

        if os.path.exists(path):
            os.remove(path)

        return True

    def install_steamcmd(self):
        """
            installs steamcmd
        """
        self._logger.info("installing steamcmd ...")

        steamcmd_tar = self._steamcmd_url.split("/")[-1]
        if not os.path.exists(self._steamcmd_path):
            os.makedirs(self._steamcmd_path)

        steamcmd_tar = os.path.join(
            self._steamcmd_path,
            steamcmd_tar
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

    def download_sourcemod(self):
        """
            download sourcemod
        """
        self._logger.info("downloading sourcemod ...")
        return self.download(
            self._sourcemod_url,
            os.path.join(self._root_dir, "csgo")
        )

    def unpack_sourcemod(self):
        """
            unpack sourcemod
        """
        self._logger.info("unpacking sourcemod ...")
        sourcemod_tar = self._sourcemod_url.split("/")[-1]
        dst = os.path.join(self._root_dir, "csgo")
        ret = self.unpack(sourcemod_tar, dst)
        os.remove(os.path.join(dst, sourcemod_tar))

        return ret

    def install_sourcemod(self):
        """
            install sourcemod to csgo root dir
        """
        self._logger.info("installing sourcemod ...")
        if not self.download_sourcemod():
            self._logger.error("could not download sourcemod!")
            return False

        if not self.unpack_sourcemod():
            self._logger.error("could not unpack sourcemod!")
            return False

        return True

    def download_metamod(self):
        """
            download metamod
        """
        self._logger.info("downloading metamod ...")
        return self.download(
            self._metamod_url,
            os.path.join(self._root_dir, "csgo")
        )

    def unpack_metamod(self):
        """
            unpack metamod
        """
        self._logger.info("unpacking metamod ...")
        metamod_tar = self._metamod_url.split("/")[-1]
        dst = os.path.join(self._root_dir, "csgo")
        ret = self.unpack(metamod_tar, dst)
        os.remove(os.path.join(dst, metamod_tar))

        return ret

    def install_metamod(self):
        """
            install metamod to csgo root dir
        """
        self._logger.info("installing metamod ...")
        if not self.download_metamod():
            self._logger.error("could not download metamod!")
            return False

        if not self.unpack_metamod():
            self._logger.error("could not unpack metamod!")
            return False

        metamod_vdf = os.path.join(self._root_dir, "csgo/addons/metamod.vdf")
        with open(metamod_vdf, "w") as _file:
            _file.write('"Plugin"\n')
            _file.write('{\n')
            _file.write('\t"file"  "../csgo/addons/metamod/bin/server"\n')
            _file.write('}\n')

        return True

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

    def install_plugins(self):
        """
            install sourcemod plugins
        """
        self._logger.info("installing plugins ...")

        plugins = self._config.get("sourcemod.plugins")

        for plugin in plugins:
            self._logger.info("installing plugin '%s' ..." % plugin)
            plugin_path = os.path.join(self._data_path, "plugins", plugin)

            if os.path.exists(plugin_path + ".smx"):
                plugin_path = plugin_path + ".smx"

            if not os.path.exists(plugin_path):
                self._logger.error(
                    "could not find plugin files for '%s'" % plugin_path
                )
                continue

            src = plugin_path
            dst = self._config.get("csgo.root_directory")

            if plugin_path.endswith(".smx"):
                dst = os.path.join(
                    self._config.get("csgo.root_directory"),
                    "csgo/addons/sourcemod/plugins/"
                )
                shutil.copy2(src, dst)
                continue

            self.copy_tree(src, dst)

        self._logger.info("simple plugins successfully installed")
        return True

    def dowload_map(self, map_name):
        """
            download map from fastdl server
        """
        fastdl_url = self._config.get("csgo.fastdl_url")
        url = fastdl_url + "maps/" + map_name + ".bsp.bz2"
        maps_dir = os.path.join(
            self._config.get("csgo.root_directory"),
            "csgo/maps"
        )
        return self.download(url, maps_dir)

    def unpack_maps(self):
        """
            unpack all maps (*.bz2)
            in csgo/maps
        """
        maps_dir = os.path.join(
            self._config.get("csgo.root_directory"),
            "csgo/maps"
        )

        for map_file in os.listdir(maps_dir):
            if not map_file.endswith(".bsp.bz2"):
                continue

            self._logger.info("unpacking map '%s' ..." % map_file)

            ret = self.open_subprocess(
                [
                    "bzip2",
                    "-d",
                    map_file
                ],
                maps_dir
            )

            if not ret:
                return False

        return True

    def install_maps(self):
        """
            install maps if maps are not
            already in maps dir
        """
        maps_dir = os.path.join(
            self._config.get("csgo.root_directory"),
            "csgo/maps"
        )

        maps_installed = os.listdir(maps_dir)

        for map in self._config.get("csgo.maps"):
            map_name = map + ".bsp"

            if map_name in maps_installed:
                self._logger.info("map '%s' already installed" % map_name)
                continue

            self._logger.info("installing map '%s' ..." % map_name)
            ret = self.dowload_map(map)

            if not ret:
                return ret

        if not self.unpack_maps():
            return False

        self._logger.info("writing maps to maplist.txt & mapcycle.txt ...")

        maplist_file = os.path.join(
            self._config.get("csgo.root_directory"),
            "csgo/maplist.txt"
        )

        mapcycle_file = os.path.join(
            self._config.get("csgo.root_directory"),
            "csgo/mapcycle.txt"
        )

        with open(maplist_file, "w") as maplist:
            for map in self._config.get("csgo.maps"):
                maplist.write(map)
                maplist.write("\n")

        shutil.copy2(maplist_file, mapcycle_file)

        return True

    def install_config(self):
        """
            install/write specific config files
        """
        if not self.write_server_config():
            self._logger.error("could not write server config")
            return False

        return True

    def write_server_config(self):
        """
            write config server.cfg
        """
        server_cfg_file = os.path.join(
            self._config.get("csgo.root_directory"),
            "csgo/cfg/server.cfg"
        )

        self._logger.info("generating '%s' ..." % server_cfg_file)

        with open(server_cfg_file, "w") as config_file:
            server_vars = self._config.get("server_config")
            for key, value in server_vars.iteritems():
                config_file.write(
                    '%s "%s"\n' % (key, value)
                )

        return True

    def create_start_script(self):
        """
            create start.sh script in csgo root dir
            example:
            ./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 0
            +map am_must2 -tickrate 128 -maxplayers_override 32 -condebug
        """
        gametype = self._config.get("csgo.game_type")
        gamemode = self._config.get("csgo.game_mode")
        start_map = self._config.get("csgo.map")
        tickrate = self._config.get("csgo.tickrate")
        max_players = self._config.get("csgo.max_players")
        port = self._config.get("csgo.port")

        cmd = os.path.join(self._root_dir, "srcds_run")
        args = [
            "-game csgo",
            "-console",
            "-usercon"
        ]

        if gametype:
            arg = "%s %s" % (Parameters.GAME_TYPE, gametype)
            args.append(arg)
        if gamemode:
            arg = "%s %s" % (Parameters.GAME_MODE, gamemode)
            args.append(arg)
        if start_map:
            arg = "%s %s" % (Parameters.MAP, start_map)
            args.append(arg)
        if tickrate:
            arg = "%s %s" % (Parameters.TICKRATE, tickrate)
            args.append(arg)
        if max_players:
            arg = "%s %s" % (Parameters.MAX_PLAYERS, max_players)
            args.append(arg)
        if port:
            arg = "%s %s" % (Parameters.PORT, port)
            args.append(arg)

        start_script_path = os.path.join(self._root_dir, "start.sh")
        arg_string = " ".join(args)

        with open(start_script_path, "w") as start_script_file:
            start_script_file.write("%s %s" % (cmd, arg_string))

        # set execute permission
        sta = os.stat(start_script_path)
        os.chmod(start_script_path, sta.st_mode | stat.S_IEXEC)

        return True
