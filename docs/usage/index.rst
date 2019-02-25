.. _role_advanced_usage:

Advanced Usage
=======================

.. toctree::
   :maxdepth: 2

   configure
   role-variables
   maintenance/index


For First usage of the Role crate a Ansible Playbook Project, with a structure like this:

.. code-block:: shell

    .
    ├── inventories
    │   ├── prod
    │   │   └── hosts.yml
    │   └── test
    │       └── hosts.yml
    ├── pluginlist.yml
    ├── provision-minecraft-master.yml
    ├── requirements.yml
    └── Vagrantfile

*(The* ``Vagrantfile`` *is only for a local TestEnv needet)*

List this ``role`` under the ``requirements.yml`` file.

.. code-block:: yaml

    ...
    - name: nolte.minecraft
      version: 4.3.2.dev
    ...

.. warning::
    Please when you host the Minecraft Server at the
    internet configure somethink like ``firewalld`` for a minimal portection, and don`t publish the ``rcon.port`` to the public space!!
