.. _role_config_role:

Configure the Role
***********************************************************************

This role shoud fix two Problems, firstly :ref:`role_config_role_server` and secondly :ref:`role_config_role_plugins`.

.. _role_config_role_server:

Configure the Server
=======================================================================

This Role will be install by default a vanilla server to the configured :ref:`Server Directory <role_config_variabels-minecraft_home>`.
You will find a full list of configuration attributes on :ref:`role_config_variabels`.

Example
-----------------------------------------------------------------------

.. code:: yaml

    - hosts: minecraft
      roles:
         - { role: nolte.minecraft, minecraft_whitelist: ["jeb_", "dinnerbone"]}


.. _role_config_role_plugins:

Install Plugins
=======================================================================

The plugins will installed to the Configured :ref:`Plugins Location <role_config_variabels-minecraft_plugins>`
into a Release subfolder like ``plugins/releases/{pluginsets}/*.jar`` and finaly link to ``plugins/shared``.

The ``plugins/shared`` Directory will be linked to ``server/shared/plugins`` all Plugin Runtime-data of
your server will be stored under ``plugins/shared``, see :ref:`maintenance_structure_fs`.


.. literalinclude:: ./../../playbook_configure_vagrent.yml
   :language: yaml
   :lines: 8-28
   :caption: Example Plugin Source Config file
   :name: example-plugins-config

.. _role_config_role_plugins-download-src:

Configure Plugin Download Source
-----------------------------------------------------------------------

Directly Download a ``*.jar`` from a Webserver, like ``media.forgecdn.net``.

``type`` (*optional*)
   default direct jar

.. _role_config_role_plugins-jenkins:

   ``"jenkins_latest"`` used for load the latest successful build.

.. _role_config_role_plugins-archive:

   ``"archive"`` used for load and unpack some Archive from remote.

``src``
   The Download Source from the Plugin.

``dest`` (*optional*)
   The local jar name, like ``PermissionsEx.jar``

``force`` (*optional*)
   overwrite allways existing plugins, (default: ``false``).

``validate_certs`` (*optional*)
   If ``false``, SSL certificates will not be validated, look (`Ansible Doc, validate_certs <https://docs.ansible.com/ansible/latest/modules/get_url_module.html>`_) (default: ``true``).

``jenkins_artefact_path`` (*optional*)
   | system group Minecraft runs as (default: ``/artifact/target``)
   | only usable with ``type: "jenkins_latest"``

.. _role_config_role_plugins-configure:

``config`` (*optional*)
  | To automatical configure a plugin create a ``Jinja`` templatefile at your Playbook ``templates`` folder, and add a ``config:`` entry.
  | The ``dest:`` path is relative to the ``plugins/shared`` folder.


  .. code-block:: yaml
     :caption: You can set a list of ``dict`s`` like:
     :name: example-plugin-conf-template

     ...
     config:
       - src: "{{ playbook_dir }}/templates/config_permissionex.yml.j2"
         dest: PermissionsEx/config.yml
     ...
