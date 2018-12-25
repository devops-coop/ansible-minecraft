Configure the Role
=============================

.. code-block:: bash

    [root@centos7 minecraft]# tree -L 3
    .
    |-- plugins
    |   |-- current -> /opt/minecraft/plugins/releases/minimal
    |   |-- releases
    |   |   `-- minimal
    |   `-- shared
    |       |-- PermissionsEx
    |       |-- PermissionsEx-1.23.4.jar -> /opt/minecraft/plugins/releases/minimal/PermissionsEx-1.23.4.jar
    |       |-- PluginMetrics
    |       |-- TNE.jar -> /opt/minecraft/plugins/releases/minimal/TNE.jar
    |       |-- TheNewEconomy
    |       |-- Updater
    |       |-- Vault
    |       |-- Vault.jar -> /opt/minecraft/plugins/releases/minimal/Vault.jar
    |       `-- bStats
    `-- server
        |-- current -> /opt/minecraft/server/releases/1.9
        |-- releases
        |   `-- 1.9
        `-- shared
            |-- ...
            |-- plugins -> /opt/minecraft/plugins/shared
            |-- spigot.jar -> /opt/minecraft/server/current/spigot-1.9.jar
            `-- ...


Configure the Server
-----------------------------

**TBD**


Install Plugins
-------------------------------

| The Problems by many plugins is the copatibility.
| The most plugins have a ``*.jar``` and a configuration Folder.
| Plugin updates shoud only change the used ``*.jar``.
| The config of a plugin will be placed under ``plugins/shared``.
| the jars placed under ``plugins/releases/{pluginsets}/*.jar`` and will finaly link to ``plugins/shared``

| finaly the ``plugins/shared`` will be linked to ``server/shared/plugins``
| all pluginruntime data of your server will be stored under ``plugins/shared``

**example config:**

.. code-block:: yaml

    minecraft_plugins_set_version: "minimal"
    minecraft_plugin_sets:
      minimal:
        vault:
          src: https://media.forgecdn.net/files/2615/750/Vault.jar
        permissionsEx:
          src: https://media.forgecdn.net/files/909/154/PermissionsEx-1.23.4.jar
          config:
            - src: config_permissionex.yml.j2
              dest: PermissionsEx/config.yml
        tne:
          src: https://github.com/TheNewEconomy/TNE-Bukkit/releases/download/Beta-1.1.3/Beta.1.1.3.zip
          type: "archive"

Configure Plugin
**************************************

| To automatical configure a plugin create a ``Jinja`` templatefile at your Playbook ``templates`` folder, and add a ``config:`` entry.
| The ``dest:`` path is relative to the ``plugins/shared`` folder.
