Ansible Role for Managing your Minecraft Server
==================================================

This role installs `Minecraft <https://minecraft.net/>`__ or `Spigot <https://www.spigotmc.org/>`__ and configures it to run under `systemd <https://wiki.freedesktop.org/www/Software/systemd/>`__ or `Supervisor <http://supervisord.org/>`__.
Its recomendet to use the ``systemd`` process managment.

.. note::
  | For all steps (Development,starting the Server and executing tests) the User must accept the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`__, by own configured property!
  | by example setting a envierment property like ``export mc_accept_eula=true``

This Documentation shoud be describe how you use and develop this Ansible Role.
You find a list of possible role configurations at :ref:`role_config_variabels`.

.. toctree::
   :caption: Table of Contents
   :name: mastertoc
   :maxdepth: 1

   Readme <readme>
   usage/index
   development/index


Structure
----------------------------------------------------

A finished installation can be looks like:

.. literalinclude:: install-structure-tree.txt
  :language: bash
