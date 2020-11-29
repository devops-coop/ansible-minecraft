.. _readme:

ansible-minecraft
=================

**This is a fork from the
https://github.com/devops-coop/ansible-minecraft/ Project, thanks for
the basement!!!**

|CircleCI| |Build Status| |Install from Ansible Galaxy| |Chat on
gitter.im| |image1| |Documentation Status|

This role installs `Minecraft`_ or `Spigot`_ and configures it to run
under `systemd`_ or `Supervisor`_.

Features
--------

-  supports `vanilla Minecraft`_ and `Spigot <https://spigotmc.org/>`__
-  supports Debian >9, Ubuntu 14.04, Ubuntu 16.04, Ubuntu 18.04, CentOS
   7, Fedora 29
-  safely stops the server using `stop`_ when running under **systemd**
-  uses `Docker`_ and `Molecule`_ to run integration tests
-  manages user ACLs
-  manages Bukkit/Spigot Plugins
-  manages ``server.properties``
-  hooks: include arbitrary tasks at specific stages during execution

Out of Role Scop
~~~~~~~~~~~~~~~~

-  executing backups and recovery
-  healthy checks like `Minecraft-Region-Fixer`_
-  handle utility services like `filebeat`_ or `prometheus`_
-  install additional Tools like `rcon-cli`_.

**All of this is needet but not a part of this role!**, *you will find
examples at*\ `nolte/minecraft-infrastructure`_\ *.*

Usage
-----

By default this role will be install a Vanilla Minecraft Server.

Install
~~~~~~~

::

      ansible-galaxy install nolte.minecraft

or add this to your ``requirements.yml``

::

   - name: nolte.minecraft
     version: v5.0.12.dev

and execute ``ansible-galaxy install -r requirements.yml``

Use
~~~

::

     - hosts: minecraft
       roles:
          - { role: nolte.minecraft, minecraft_whitelist: ["jeb_", "dinnerbone"]}

Requirements
------------

-  Python 3.x on the Ansible control machine to generate user ACLs
-  Ansible 2.7.0+ on the control machine to fetch the Minecraft version

Contributing
------------

The best way to contribute is to use this role to deploy your own
Minecraft server! We really appreciate bug

.. _Minecraft: https://minecraft.net/
.. _Spigot: https://www.spigotmc.org/
.. _systemd: https://wiki.freedesktop.org/www/Software/systemd/
.. _Supervisor: http://supervisord.org/
.. _vanilla Minecraft: https://minecraft.net
.. _stop: http://minecraft.gamepedia.com/Commands#stop
.. _Docker: https://www.docker.com/
.. _Molecule: https://molecule.readthedocs.io/
.. _Minecraft-Region-Fixer: https://github.com/Fenixin/Minecraft-Region-Fixer
.. _filebeat: https://www.elastic.co/de/products/beats/filebeat
.. _prometheus: https://github.com/prometheus/node_exporter
.. _rcon-cli: https://github.com/itzg/rcon-cli
.. _nolte/minecraft-infrastructure: https://github.com/nolte/minecraft-infrastructure

.. |CircleCI| image:: https://circleci.com/gh/nolte/ansible-minecraft.svg?style=svg
   :target: https://circleci.com/gh/nolte/ansible-minecraft
.. |Build Status| image:: https://travis-ci.org/nolte/ansible-minecraft.svg?branch=develop
   :target: https://travis-ci.org/nolte/ansible-minecraft
.. |Install from Ansible Galaxy| image:: https://img.shields.io/badge/role-nolte.minecraft-blue.svg
   :target: https://galaxy.ansible.com/nolte/minecraft
.. |Chat on gitter.im| image:: https://badges.gitter.im/gitterHQ/gitter.png
   :target: https://gitter.im/devops-coop/ansible-minecraft
.. |image1| image:: https://img.shields.io/github/release/nolte/ansible-minecraft.svg
   :target: https://github.com/nolte/ansible-minecraft
.. |Documentation Status| image:: https://readthedocs.org/projects/ansible-minecraft/badge/?version=master
   :target: https://ansible-minecraft.readthedocs.io/en/master

