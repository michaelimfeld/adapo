# csgo server assembler/installer

This python application has the goal to setup/install a Counter-Strike: Global Offensive Servers inlcuding metamod, sourcemod and its plugins by only reading a text based configuration file.
To install custom sourcemod plugins an additional data folder is required. (see sourcemod data)

This software will be designed for deploying multiple CS:GO Servers with SaltStack.

## usage

The following command will assemble/install all cs:go servers configured in "/etc/adapo/servers.d/".

    adapo install

## sourcemod data
### plugins
There are two types of plugins:
 - simple
 - complex

For a simple plugin only the compiled .smx plugin binary is needed. simple.

Example directory structure:

    data/plugins/simpleplugin.smx

Complex plugins need to be stored as a directory named like the plugin itself containing the whole tree from csgo root dir.

Example directory structure:

    data/plugins/complexplugin/csgo/addons/plugins/complexplugin.smx
    data/plugins/complexplugin/csgo/addons/configs/complex.cfg
    data/plugins/complexplugin/csgo/cfg/sourcemod/complexplugin/plugin.cfg

The data directory can be set in the global adapo configuration (/etc/adapo/main.cfg)
