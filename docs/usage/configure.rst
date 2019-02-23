.. _role_config_role:

Configure the Role
=============================

.. literalinclude:: ../install-structure-tree.txt
   :language: bash


Configure the Server
-----------------------------


Example
`````````````````````````````````````````````````````````````````

.. code:: yaml

    - hosts: minecraft
      roles:
         - { role: nolte.minecraft, minecraft_whitelist: ["jeb_", "dinnerbone"]}


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
        multiverse:
          src: https://ci.onarandombox.com/job/Multiverse-SignPortals/lastSuccessfulBuild
          type: "jenkins_latest"
          validate_certs: false


Configure Plugin
`````````````````````````````````````````````````````````````````

| To automatical configure a plugin create a ``Jinja`` templatefile at your Playbook ``templates`` folder, and add a ``config:`` entry.
| The ``dest:`` path is relative to the ``plugins/shared`` folder.
