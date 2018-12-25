Ansible Role for Managing your Minecraft Server
==================================================

This role installs `Minecraft <https://minecraft.net/>`__ or `Spigot <https://www.spigotmc.org/>`__ and configures it to run under `systemd <https://wiki.freedesktop.org/www/Software/systemd/>`__ or `Supervisor <http://supervisord.org/>`__.
Its recomendet to use the ``systemd`` process managment.

For all steps (Development,starting the Server and executing tests) the User must accept the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`__, by own configured property!

Overview
-----------------------------

.. toctree::
   :maxdepth: 2

   usage/index
   development/index



Role scope Description
-----------------------------

- initial installation
- handle mc server version updates
- handle plugins

Out of Scope
*******************************

- executing backups and recovery
- healthy checks like `Minecraft-Region-Fixer <https://github.com/Fenixin/Minecraft-Region-Fixer>`_
- handle utility services like `filebeat <https://www.elastic.co/de/products/beats/filebeat>`_ or `prometheus <https://github.com/prometheus/node_exporter>`_
- install additional Tools like `rcon-cli <https://github.com/itzg/rcon-cli>`_.

**All of this is needet but not a part of this role!**


A finished installation can be looks like:

.. code-block:: shell

    [xxxx@minecraft /]$ tree -d -L 4 /opt/
    /opt/
    └── minecraft
        └── server
            ├── current -> /opt/minecraft/server/releases/1.13.1
            ├── releases
            │   └── 1.13.1
            └── shared
                ├── logs
                ├── plugins
                ├── world
                ├── world_flat
                ├── world_nether
                ├── world_survival
                ├── world_survival_nether
                └── world_the_end
