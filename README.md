# ansible-minecraft


**This is a fork from the https://github.com/devops-coop/ansible-minecraft/ Project, thanks for the basement!!!**


[![molecule e2e](https://github.com/nolte/ansible-minecraft/workflows/molecule%20e2e/badge.svg)](https://github.com/nolte/ansible-minecraft/actions?query=workflow%3A%22molecule+e2e%22) [![Install from Ansible Galaxy](https://img.shields.io/badge/role-nolte.minecraft-blue.svg)](https://galaxy.ansible.com/nolte/minecraft) [![Chat on gitter.im](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/devops-coop/ansible-minecraft) [![](https://img.shields.io/github/release/nolte/ansible-minecraft.svg)](https://github.com/nolte/ansible-minecraft) [![Documentation Status](https://readthedocs.org/projects/ansible-minecraft/badge/?version=master)](https://ansible-minecraft.readthedocs.io/en/master)


This role installs [Minecraft](https://minecraft.net/) or [Spigot](https://www.spigotmc.org/) and configures it to run under [systemd](https://wiki.freedesktop.org/www/Software/systemd/).


## Features

-  supports [vanilla Minecraft](https://minecraft.net) and [Spigot](https://spigotmc.org/)
-  supports Debian >9, Ubuntu 14.04, Ubuntu 16.04, Ubuntu 18.04, CentOS 7 & 8, Fedora 29
-  safely stops the server using [stop](http://minecraft.gamepedia.com/Commands#stop) when running under **systemd**
-  uses [Docker](https://www.docker.com/) and [Molecule](https://molecule.readthedocs.io/) to run integration tests
-  manages user ACLs
-  manages Bukkit/Spigot Plugins
-  manages ``server.properties``
-  hooks: include arbitrary tasks at specific stages during execution

### Out of Role Scop

- install a *Java Runtime*, this must be done, before you use this Role, you can use [nolte/ansible-role-msopenjdk](https://github.com/nolte/ansible-role-msopenjdk) for example.
- executing backups and recovery
- healthy checks like [Minecraft-Region-Fixer](https://github.com/Fenixin/Minecraft-Region-Fixer)
- handle utility services like [filebeat](https://www.elastic.co/de/products/beats/filebeat) or [prometheus](https://github.com/prometheus/node_exporter)
- install additional Tools like [rcon-cli](https://github.com/itzg/rcon-cli).

**All of this is needet but not a part of this role!**, _you will find examples at [nolte/minecraft-infrastructure](https://github.com/nolte/minecraft-infrastructure)._

## Usage

 By default this role will be install a Vanilla Minecraft Server.

### Install

```
   ansible-galaxy install nolte.minecraft
```

or add this to your ``requirements.yml``

```
- name: nolte.minecraft
```

and execute ``ansible-galaxy install -r requirements.yml``

### Use

```
  - hosts: minecraft
    roles:
       - { role: nolte.minecraft, minecraft_whitelist: ["jeb_", "dinnerbone"]}
```

## Requirements

-  Python 3.x on the Ansible control machine to generate user ACLs
-  Ansible 2.7.0+ on the control machine to fetch the Minecraft version
-  Existing Compatible Java Runtime for start and install Minecraft on target System.


## Contributing

The best way to contribute is to use this role to deploy your own Minecraft server! We really appreciate bug reports from the wild.

If you'd like to help with the project itself, here are some other ways you can contribute:

-  Add support for additional servers like [Cuberite](https://cuberite.org/).
-  Write integration tests for Minecraft- or Spigot-specific configuration.
-  Share useful hooks.
-  Fixing Typos ...

## License

Apache 2.0

## Disclaimer

For execute a automatical installation you must accept the [Minecraft EULA](https://account.mojang.com/documents/minecraft_eula). Be aware that by using this role, you implicitly accept the same EULA.
You can handle the acception by using a Environment Property like: ``export mc_accept_eula=true`` the default is ``false`` for disagree.
