ansible-minecraft
=================

** This is a fork from the https://github.com/devops-coop/ansible-minecraft/ Project, thanks for the basement!!!**

|Install from Ansible Galaxy| |Travis CI build status| |Chat on gitter.im|

This role installs `Minecraft <https://minecraft.net/>`__ or `Spigot <https://www.spigotmc.org/>`__ and configures it to run under `systemd <https://wiki.freedesktop.org/www/Software/systemd/>`__ or `Supervisor <http://supervisord.org/>`__.

**If you're viewing this at** https://github.com/devops-coop/ansible-minecraft/**, you're reading the documentation for the master branch.** `View documentation for the latest release (3.1.0). <https://github.com/devops-coop/ansible-minecraft/tree/v3.1.0#ansible-minecraft>`__

Requirements
------------

-  **Optional:** Python 2.7 on the Ansible control machine to generate user ACLs
-  **Optional:** Ansible 2.0.2+ or ``curl`` on the control machine to fetch the latest Minecraft version

Install
-------

::

   ansible-galaxy install devops-coop.minecraft


Features
--------

-  supports `vanilla Minecraft <https://minecraft.net>`__ and `Spigot <https://spigotmc.org/>`__
-  supports Debian 8, Ubuntu 14.04, Ubuntu 16.04, and RHEL/CentOS 7
-  supports different process supervisors on different platforms

   +----------------+------------------+------------------+
   | OS             |     Supervisor   |      systemd     |
   |                +---------+--------+---------+--------+
   |                | vanilla | spigot | vanilla | spigot |
   +================+=========+========+=========+========+
   | Debian 8       | ✓       | ✓      | ✓       | ✓      |
   +----------------+---------+--------+---------+--------+
   | Ubuntu 14.04   | ✓       | ✓      | ✗       | ✗      |
   +----------------+---------+--------+---------+--------+
   | Ubuntu 16.04   | ✓       | ✓      | ✓       | ✓      |
   +----------------+---------+--------+---------+--------+
   | Ubuntu 18.04   | ✗       | ✗      | ✓       | ✗      |
   +----------------+---------+--------+---------+--------+
   | CentOS 7       | ✗       | ✗      | ✓       |  ✓     |
   +----------------+---------+--------+---------+--------+

-  safely stops the server using `stop <http://minecraft.gamepedia.com/Commands#stop>`__ when running under **systemd**
-  uses `Docker <https://www.docker.com/>`__ and `Molecule <https://molecule.readthedocs.io/>`__ to run integration tests
-  manages user ACLs
-  manages ``server.properties``
-  hooks: include arbitrary tasks at specific stages during execution

Versioning
----------

This project follows `semantic versioning <http://semver.org/>`__.

In the context of semantic versioning, consider the role contract to be defined by the role variables.

-  Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
-  Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
-  Bug fixes will increase the **patch** version.

Refer to the `change log <CHANGELOG.rst>`__ for upcoming changes.

Role variables
--------------

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

``minecraft_home``
   directory to install Minecraft to (default: ``/opt/minecraft``)

``minecraft_max_memory``
   Java max memory (``-Xmx``) to allocate (default: ``1024M``)

``minecraft_initial_memory``
   Java initial memory (``-Xms``) to allocate (default: ``1024M``)

``minecraft_service_name``
   systemd service name or Supervisor program name (default: ``minecraft``)

``minecraft_supervisor_name``
   **DEPRECATED:** Supervisor program name (default: ``{{ minecraft_service_name }}``)

``minecraft_process_control``
   Choose between ``systemd`` and ``supervisor`` (default: ``systemd``).

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

```minecraft_server_java_ops```
   additional java ops like remote debug ``-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005
``  (default: *none*)

Hooks and run stages
--------------------

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

Example
-------

.. code:: yaml

    - hosts: minecraft
      roles:
         - { role: devops-coop.minecraft, minecraft_whitelist: ["jeb_", "dinnerbone"]}

Contributing
------------

The best way to contribute is to use this role to deploy your own Minecraft server! We really appreciate bug reports from the wild.

If you'd like to help with the project itself, here are some other ways you can contribute:

-  Add support for additional servers like `Cuberite <https://cuberite.org/>`__.
-  Write integration tests for Minecraft- or Spigot-specific configuration.
-  Share useful hooks.
-  Fixing Typos ...

Testing
~~~~~~~
Testing can be done using the provided Vagrantfile or by installing `Docker <https://docs.docker.com/engine/installation/>`__ and use `Molecule <https://molecule.readthedocs.io/>`__ locally.

For execute the molecule test you can use the Docker Image described at `Molecule <https://molecule.readthedocs.io/en/latest/examples.html#docker>`__ page.

.. code:: bash

     docker run --rm -it \
         -v $(pwd):/tmp/$(basename "${PWD}"):ro \
         -v /var/run/docker.sock:/var/run/docker.sock \
         -e mc_accept_eula=${mc_accept_eula} \
         -w /tmp/$(basename "${PWD}") \
         retr0h/molecule:latest \
         sudo molecule test --all

after execute drink a pot of tee, coffee or some beer, all molecule scenarios will be run more than 40 minute

Testing with Vagrant
"""""""""""""""""""""
This role includes a Vagrantfile used with a Docker-based test harness that approximates the Travis CI setup for integration testing. Using Vagrant allows all contributors to test on the same platform and avoid false test failures due to untested or incompatible docker versions.

1. Install `Vagrant <https://www.vagrantup.com/>`__ and `VirtualBox <https://www.virtualbox.org/>`__.
1.1 Accept the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`__ with setting a Environment Property like: ```export mc_accept_eula=true && vagrant up```

2. Run ``vagrant up`` from the same directory as the Vagrantfile in this repository.

Now you can Connect with your Game again the Testserver on ``localhost:25565`` and test your server.

3. for manual lookups you can connect over SSH into the VM with: ``vagrant ssh``

License
-------

Apache 2.0

Disclaimer
----------

For execute a automatical installation you must accept the accepts the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`__. Be aware that by using this role, you implicitly accept the same EULA.
You can handle the acception by using a Environment Property like: ```export mc_accept_eula=true```

--To automate the installation, this role automatically accepts the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`__. Be aware that by using this role, you implicitly accept the same EULA.--

.. |Travis CI build status| image:: https://travis-ci.org/nolte/ansible-minecraft.svg?branch=master
    :target: https://travis-ci.org/nolte/ansible-minecraft
.. |Install from Ansible Galaxy| image:: https://img.shields.io/badge/role-nolte.minecraft-blue.svg
    :target: https://galaxy.ansible.com/nolte/minecraft/
.. |Chat on gitter.im| image:: https://badges.gitter.im/gitterHQ/gitter.png
    :target: https://gitter.im/devops-coop/ansible-minecraft
