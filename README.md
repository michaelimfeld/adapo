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
