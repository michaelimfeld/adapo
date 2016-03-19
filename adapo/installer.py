"""
    Main Server Installer Module
"""

import os
import vdf
import stat
import shutil
from collections import OrderedDict
from adapo.logger import Logger
from adapo.config import Config
from adapo.parameters import Parameters
from adapo.resourcemanager import ResourceManager


class Installer(object):
    """
        CS:GO Server Installer
    """

    LOG_FILE = "/tmp/adapo_installer.log"
    ADAPO_CONF = "/etc/adapo/main.cfg"

    def __init__(self, config_path):
        self._log = Logger()

        # load global adapo configuration
        self._global_config = Config(self.ADAPO_CONF)

        self._steamcmd_url = self._global_config.steamcmd_dl_url
        self._steamcmd_path = self._global_config.steamcmd_path

        if not self._steamcmd_url or not self._steamcmd_path:
            self._log.error(
                "steamcmd config attrs are required to"
                " install a csgo server"
            )
            exit(1)

        if not os.path.exists(self._steamcmd_path):
            os.makedirs(self._steamcmd_path)

        self._metamod_url = self._global_config.metamod_dl_url
        self._sourcemod_url = self._global_config.sourcemod_dl_url
        if not self._steamcmd_url or not self._steamcmd_path:
            self._log.error(
                "source & metamode urls are required to install a csgo server"
            )
            exit(1)

        # load specific cs:go server configuration
        self._config = Config(config_path)
        if not self._config.csgo:
            self._log.error(
                "configuration section 'csgo' not found!"
            )
            exit(1)

        self._root_dir = self._config.csgo.get("root_directory")
        if not self._root_dir:
            self._log.error(
                "root directory not set"
            )
            exit(1)



        self._resourcemanager = ResourceManager()

    def install(self):
        """
            install csgo server
        """
        if not self.install_steamcmd():
            self._log.error(
                "steamcmd installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("steamcmd successfully installed")

        if not self.install_csgo():
            self._log.error(
                "csgo installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("csgo successfully installed")

        if not self.install_metamod():
            self._log.error(
                "metamod installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("metamod successfully installed")

        if not self.install_sourcemod():
            self._log.error(
                "sourcemod installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("sourcmod successfully installed")

        if not self.install_plugins():
            self._log.error(
                "plugin installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("plugins successfully installed")

        if not self.install_maps():
            self._log.error(
                "map installation failed, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("maps successfully installed")

        if not self.write_server_config():
            self._log.error(
                "could not install config!, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            return False
        self._log.info("server config successfully installed")

        if not self.create_start_script():
            self._log.error(
                "could not create start script!, "
                "check '%s' for errors!" % self.LOG_FILE
            )
            self._log.info("start script successfully written")

        return True

    def uninstall(self):
        """
            uninstall csgo server
        """
        # FIXME: Implement uninstall
        self._log.info("uninstall not implemented yet")

    def install_csgo(self):
        """
            install csgo server
        """
        self._log.info("installing csgo with steamcmd ...")

        if not os.path.exists(self._root_dir):
            os.makedirs(self._root_dir)

        return self._resourcemanager.open_subprocess(
            [
                "./steamcmd.sh",
                "+login",
                "anonymous",
                "+force_install_dir",
                self._root_dir,
                "+app_update",
                "740",
                "+quit"
            ],
            self._steamcmd_path
        )

    def download_steamcmd(self):
        """
            download steamcmd.tar.gz
        """
        self._log.info("downloading steamcmd ...")

        return self._resourcemanager.download(
            self._steamcmd_url,
            self._steamcmd_path
        )

    def clean_steamcmd(self):
        """
            clean steamcmd directory
        """
        self._log.info("cleaning up steamcmd directory ...")

        steamcmd_tar = self._steamcmd_url.split("/")[-1]
        path = os.path.join(self._steamcmd_path, steamcmd_tar)

        if os.path.exists(path):
            os.remove(path)

        return True

    def install_steamcmd(self):
        """
            installs steamcmd
        """
        self._log.info("installing steamcmd ...")

        if not os.path.exists(self._steamcmd_path):
            os.makedirs(self._steamcmd_path)

        steamcmd_tar = self._steamcmd_url.split("/")[-1]
        steamcmd_tar = os.path.join(
            self._steamcmd_path,
            steamcmd_tar
        )

        if os.path.exists(steamcmd_tar):
            self._log.error("steamcmd_linux.tar.gz already exists!")
            return False

        if not self.download_steamcmd():
            self._log.error("could not download steamcmd!")
            return False
        self._log.info("steamcmd successfully downloaded")

        if not self._resourcemanager.unpack(steamcmd_tar, self._steamcmd_path):
            self._log.error("could not unpack steamcmd!")
            return False
        self._log.info("steamcmd successfully unpacked")

        if not self.clean_steamcmd():
            self._log.error("could not clean steamcmd!")
            return False
        self._log.info("steamcmd successfully cleaned")

        return True

    def download_sourcemod(self):
        """
            download sourcemod
        """
        sourcemod_tar = self._sourcemod_url.split("/")[-1]
        sourcemod_tar_path = os.path.join(self._root_dir, "csgo", sourcemod_tar)

        if os.path.exists(sourcemod_tar_path):
            self._log.info(
                "sourcemod already cached, if you want to redownload it"
                " remove the sourcemod tar file: '{0}' ..."
                .format(sourcemod_tar_path)
            )
            return sourcemod_tar_path

        self._log.info("downloading sourcemod ...")
        return self._resourcemanager.download(
            self._sourcemod_url,
            os.path.join(self._root_dir, "csgo")
        )

    def install_sourcemod(self):
        """
            install sourcemod to csgo root dir
        """
        self._log.info("installing sourcemod ...")
        sourcemod_tar = self.download_sourcemod()
        if not sourcemod_tar:
            self._log.error("could not download sourcemod!")
            return False

        dst = "/".join(sourcemod_tar.split("/")[:-1])
        if not self._resourcemanager.unpack(sourcemod_tar, dst):
            self._log.error("could not unpack sourcemod!")
            return False

        if not self.write_admins_config():
            self._log.error("could not write admins_simple.ini")
            return False
        self._log.info("admins_simple.ini successfully written")

        if not self.write_databases_config():
            self._log.error("could not write databases.cfg")
            return False
        self._log.info("databases.cfg successfully written")

        return True

    def download_metamod(self):
        """
            download metamod
        """
        metamod_tar = self._metamod_url.split("/")[-1]
        metamod_tar_path = os.path.join(self._root_dir, "csgo", metamod_tar)

        if os.path.exists(metamod_tar_path):
            self._log.info(
                "metamod already cached, if you want to redownload it"
                " remove the metamod tar file: '{0}' ..."
                .format(metamod_tar_path)
            )
            return metamod_tar_path

        self._log.info("downloading metamod ...")
        return self._resourcemanager.download(
            self._metamod_url,
            os.path.join(self._root_dir, "csgo")
        )

    def install_metamod(self):
        """
            install metamod to csgo root dir
        """
        self._log.info("installing metamod ...")
        metamod_tar = self.download_metamod()
        if not metamod_tar:
            self._log.error("could not download metamod!")
            return False

        dst = "/".join(metamod_tar.split("/")[:-1])
        if not self._resourcemanager.unpack(metamod_tar, dst):
            self._log.error("could not unpack metamod!")
            return False

        metamod_vdf = os.path.join(self._root_dir, "csgo/addons/metamod.vdf")
        with open(metamod_vdf, "w") as _file:
            _file.write('"Plugin"\n')
            _file.write('{\n')
            _file.write('\t"file"  "../csgo/addons/metamod/bin/server"\n')
            _file.write('}\n')

        return True

    def install_plugins(self):
        """
            install sourcemod plugins
        """
        self._log.info("installing plugins ...")

        sourcemod_cfg = self._config.sourcemod
        plugins = sourcemod_cfg.get("plugins")

        for plugin in plugins:
            self._log.info("installing plugin '%s' ..." % plugin)

            data_path = self._global_config.data_src_path
            if not data_path:
                return False

            plugin_path = os.path.join(data_path, "plugins", plugin)

            if os.path.exists(plugin_path + ".smx"):
                plugin_path = plugin_path + ".smx"

            if not os.path.exists(plugin_path):
                self._log.error(
                    "could not find plugin files for '%s'" % plugin_path
                )
                continue

            src = plugin_path
            dst = self._root_dir

            if plugin_path.endswith(".smx"):
                dst = os.path.join(
                    self._root_dir,
                    "csgo/addons/sourcemod/plugins/"
                )
                shutil.copy2(src, dst)
                continue

            self._resourcemanager.copy_tree(src, dst)

        self._log.info("simple plugins successfully installed")
        return True

    def dowload_map(self, map_name):
        """
            download map from fastdl server
        """
        server_cfg = self._config.server_config
        if not server_cfg:
            return False

        fastdl_url = server_cfg.get("sv_downloadurl")
        url = fastdl_url + "maps/" + map_name + ".bsp.bz2"
        maps_dir = os.path.join(
            self._root_dir,
            "csgo/maps"
        )
        return self._resourcemanager.download(url, maps_dir)

    def unpack_maps(self):
        """
            unpack all maps (*.bz2)
            in csgo/maps
        """
        maps_dir = os.path.join(
            self._root_dir,
            "csgo/maps"
        )

        for map_file in os.listdir(maps_dir):
            if not map_file.endswith(".bsp.bz2"):
                continue

            self._log.info("unpacking map '%s' ..." % map_file)

            ret = self._resourcemanager.open_subprocess(
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
            self._root_dir,
            "csgo/maps"
        )

        maps_installed = os.listdir(maps_dir)

        csgo_cfg = self._config.csgo

        for _map in csgo_cfg.get("maps"):
            map_name = _map + ".bsp"

            if map_name in maps_installed:
                self._log.info("map '%s' already installed" % map_name)
                continue

            self._log.info("installing map '%s' ..." % map_name)
            ret = self.dowload_map(_map)

            if not ret:
                return ret

        if not self.unpack_maps():
            return False

        self._log.info("writing maps to maplist.txt & mapcycle.txt ...")

        maplist_file = os.path.join(
            self._root_dir,
            "csgo/maplist.txt"
        )

        mapcycle_file = os.path.join(
            self._root_dir,
            "csgo/mapcycle.txt"
        )

        with open(maplist_file, "w") as maplist:
            for _map in csgo_cfg.get("maps"):
                maplist.write(_map)
                maplist.write("\n")

        shutil.copy2(maplist_file, mapcycle_file)

        return True

    def install_config(self):
        """
            install/write specific config files
        """
        if not self.write_server_config():
            self._log.error("could not write server config")
            return False

        return True

    def write_server_config(self):
        """
            write config server.cfg
        """
        server_cfg_file = os.path.join(
            self._root_dir,
            "csgo/cfg/server.cfg"
        )

        self._log.info("generating '%s' ..." % server_cfg_file)

        with open(server_cfg_file, "w") as config_file:
            server_vars = self._config.server_config
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
        csgo_cfg = self._config.csgo

        gametype = csgo_cfg.get("game_type")
        gamemode = csgo_cfg.get("game_mode")
        start_map = csgo_cfg.get("map")
        tickrate = csgo_cfg.get("tickrate")
        max_players = csgo_cfg.get("max_players")
        ip_addr = csgo_cfg.get("ip")
        port = csgo_cfg.get("port")

        cmd = os.path.join(self._root_dir, "srcds_run")
        args = [
            "-game csgo",
            "-console",
            "-usercon"
        ]

        if gametype is not None:
            arg = "%s %s" % (Parameters.GAME_TYPE, gametype)
            args.append(arg)
        if gamemode is not None:
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
        if ip_addr:
            arg = "%s %s" % (Parameters.IP_ADDR, ip_addr)
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

    def write_admins_config(self):
        """
            write config admins_simple.ini
        """
        admins_config_file = os.path.join(
            self._root_dir,
            "csgo/addons/sourcemod/configs/admins_simple.ini"
        )

        self._log.info("generating '%s' ..." % admins_config_file)

        sourcemod_cfg = self._config.sourcemod
        users = sourcemod_cfg.get("users")
        if not users:
            self._log.info("No users found to write to admis_simple.ini")
            return True

        with open(admins_config_file, "w") as config_file:
            for user in users:
                config_file.write(
                    '"%s" "%s"\n' % (user["steam_id"], user["flags"])
                )

        return True

    def write_databases_config(self):
        """
            write database config databases.cfg
        """
        sourcemod_cfg = self._config.sourcemod
        configured_dbs = sourcemod_cfg.get("databases")

        if not configured_dbs:
            self._log.info("no databases configured")
            return True

        database_config_path = os.path.join(
            self._root_dir,
            "csgo/addons/sourcemod/configs/databases.cfg"
        )

        db_config_file = open(database_config_path, "r")
        self._log.info(
            "loading databases configuration '%s' ..." % database_config_path
        )
        db_config = vdf.load(db_config_file, mapper=OrderedDict)
        db_config_file.close()

        for database_name, database_config in configured_dbs.iteritems():
            db_config["Databases"][database_name] = database_config

        self._log.info(
            "writing databases config '%s' ..." % database_config_path
        )
        with open(database_config_path, "w") as config_file:
            config_file.write(vdf.dumps(db_config, pretty=True))

        return True
