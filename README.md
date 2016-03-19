# CS:GO Server Assembler/Installer
[![Build Status](https://api.travis-ci.org/michaelimfeld/adapo.svg?branch=master)](https://travis-ci.org/michaelimfeld/adapo)
[![GitHub version](https://badge.fury.io/gh/michaelimfeld%2Fadapo.svg)](https://badge.fury.io/gh/michaelimfeld%2Fadapo)


This python application has the goal to setup/install Counter-Strike: Global Offensive Servers inlcuding metamod, sourcemod and its plugins by only reading a text based configuration file.
To install custom sourcemod plugins an additional data folder is required. (see sourcemod data)

This software will be designed for deploying multiple CS:GO Servers with SaltStack.

## Installation

    debuild -us -uc
    dpkg -i ../adapo_1.0_amd64.deb

## Usage

The following command will assemble/install all cs:go servers configured in "/etc/adapo/servers.d/".

    adapo install

## Configuration

An example configuration file can be found in /usr/share/adapo/.


## Sourcemod Data
### Plugins
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

You can find an example data directory in /usr/share/adapo/.
The data directory can be set in the global adapo configuration (/etc/adapo/main.cfg)
