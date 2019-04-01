.. _role_config_variabels:

Role variables
=====================================================================

The following variable defaults are defined in ``defaults/main.yml``.

``minecraft_version``
   Minecraft version to install (default: ``latest``)

   Examples:

   .. code:: yaml

       minecraft_version: latest
       minecraft_version: 1.10
       minecraft_version: 1.9.1
       minecraft_version: 16w21a

``minecraft_eula_accept``
   accept the Minecraft eula License, must accepted by the Role User (default: ``false``)

``minecraft_url``
   Minecraft download URL (default:
   ``https://s3.amazonaws.com/Minecraft.Download/versions``)

``minecraft_user``
   system user Minecraft runs as (default: ``{{ minecraft_server }}``)

``minecraft_group``
   system group Minecraft runs as (default: ``{{ minecraft_server }}``)

``minecraft_basedir``
   directory base variable for the Minecraft installation (default: ``/opt/minecraft``)

.. _role_config_variabels-minecraft_home:

``minecraft_home``
   directory to install Minecraft Server to (default: ``{{minecraft_basedir}}/server``)


.. _role_config_variabels-minecraft_plugins:

``minecraft_plugins``
   directory to install Minecraft Plugins to (default: ``{{minecraft_basedir}}/plugins``)

``minecraft_max_memory``
   Java max memory (``-Xmx``) to allocate (default: ``1024M``)

``minecraft_initial_memory``
   Java initial memory (``-Xms``) to allocate (default: ``1024M``)

``minecraft_service_name``
   systemd service name or Supervisor program name (default: ``minecraft``)

``minecraft_supervisor_name``
   **DEPRECATED:** Supervisor program name (default: ``{{ minecraft_service_name }}``)

``minecraft_whitelist``
   list of Minecraft usernames to whitelist (default: ``[]``)

``minecraft_ops``
   list of Minecraft usernames to make server ops (default: ``[]``)

``minecraft_banned_players``
   list of Minecraft usernames to ban (default: ``[]``)

``minecraft_banned_ips``
   list of IP addresses to ban (default: ``[]``)

``minecraft_server_properties``
   dictionary of server.properties entries (e.g. ``server-port: 25565``) to set (default: ``{}``)

``minecraft_server``
  choose between ``minecraft`` or ``spigot`` (default: ``minecraft``)

``minecraft_server_java_ops``
   additional java ops like remote debug ``-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005`` (default: *none*)

``minecraft_java_external_managed``
  used for skipping the java installation tasks from this role, for handle Java by external scripts/roles (default: ``false``)

.. _role_config_variabels-minecraft_external_log_conf:

Logging
---------------------------------------------------------------------------------------------------------------------------------

``minecraft_external_log_conf`` (*optional*) type Dict
  handle a external Log4j2 Config used `RollingRandomAccessFileAppender <https://logging.apache.org/log4j/2.x/manual/appenders.html#RollingRandomAccessFileAppender>`_, controlling LogRotate, Maximal LogFile Size, and maximum keeped logs.

  Examples:

  .. code:: yaml

      minecraft_external_log_conf:
        conf_file: log4j2.xml
        template: log4j2.xml.j2
        fileName: /var/log/minecraft/server.log
        filePattern: /var/log/minecraft/server_%d{yyyy-MM-dd}.log.gz
        rollover: 5
        sizeBased: 10MB



Hooks and run stages
---------------------------------------------------------------------------------------------------------------------------------

**ansible-minecraft** organizes execution into a number of run stages:

``setup``
   -  install prerequisites (e.g., Java)
   -  create Minecraft user and group

``download``
   -  fetch the latest version of from the launcher API
   -  download Minecraft

``install``
   -  symlink version to ``minecraft_server.jar``
   -  agree to EULA

``acl``
   -  configure server ACLs (whitelist, banned players, etc.)

``configure``
   -  set ``server.properties``

``start``
   -  (re)start server

You can execute custom tasks before or after specific stages. Simply specify a `task include file <https://docs.ansible.com/ansible/playbooks_roles.html#task-include-files-and-encouraging-reuse>`__ using the relevant role variable:

.. code:: yaml

    - hosts: minecraft
      roles:
        - role: devops-coop.minecraft
          minecraft_hook_before_start: "{{ playbook_dir }}/download-world-from-s3.yml"

The available hooks are:

``minecraft_hook_before_setup``
   run before ``setup`` tasks

``minecraft_hook_after_setup``
   run after ``setup`` tasks

``minecraft_hook_before_download``
   run before ``download`` tasks

``minecraft_hook_after_download``
   run after ``download`` tasks

``minecraft_hook_before_install``
   run before ``install`` tasks

``minecraft_hook_after_install``
   run after ``install`` tasks

``minecraft_hook_before_start``
   run before ``start`` tasks

``minecraft_hook_after_start``
   run after ``start`` tasks
