# csgo server assembler/installer

This python application has the goal to setup/install a Counter-Strike: Global Offensive Server inlcuding metamod, sourcemod and its plugins by only reading a text based configuration.
To install sourcemod plugins an additional data folder is required, where all the smx files and special configurations are stored.

This software will be designed for deploying multiple CS:GO Servers with SaltStack.

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

## Planned Stuff

### New Data Structure:

  - move config file(s) to /etc/
  - support multi server configs

Structure:

    /etc/adapo/adapo.conf
    /etc/adapo/servers.d/cs-01.conf
    /etc/adapo/servers.d/cs-02.conf
    /var/adapo/data/
    /var/adapo/data/plugins/

Main config file should contain:

  - steamcmd path
  - download urls for sourcemod & metamod

### Update Cronjob

Cronjob which keeps servers up to date with steamcmd.

### Init.d Script

Generate init.d script for each server configured in /etc/adapo/servers.d/.
