ansible-minecraft changelog
===========================
6.0.0
----------

Braking Change
~~~~~

- Remove the Java Installation logic from this role, because Minecraft 1.17 required Java 16, more information at (`#169 <https://github.com/nolte/ansible-minecraft/issues/169>`_). So `minecraft_java_external_managed=true` is the new Normal for this Role, using a extra role  ``nolte/ansible-role-msopenjdk <https://github.com/nolte/ansible-role-msopenjdk>`_ for install java.


5.0.0
----------
- Remove Debian Jessie and Supervisor support.

4.0.0
----------

Added
~~~~~

- (`#7 <https://github.com/devops-coop/ansible-minecraft/issues/7>`_) Support `Spigot <https://www.spigotmc.org/>`_.
- Using `Molecule <https://molecule.readthedocs.io/>`_ for Role Integration Tests, Manual Docker build removed.
- Using `Ansible Download Helper <https://docs.ansible.com/ansible/latest/modules/deploy_helper_module.html>`_ for easy version rollbacks.
- Add Support for install and handle Plugins.
- The User must Accept the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`_ by using a System Property or Playbook vars, the default is ``false``!!

Fixed
~~~~~

- (`#26 <https://github.com/devops-coop/ansible-minecraft/issues/26>`_) Latest release download failing (s3 urls depricated )


Deprecated
~~~~~~~~~~

-  Deprecate ``minecraft_supervisor_name`` in favour of ``minecraft_service_name``.

Fixed
~~~~~

- When using ``curl`` to check the latest release, execute the task locally instead of on the remote host.

3.1.0 (2016-12-10)
------------------

Added
~~~~~

- Add support for Ubuntu 16.04 LTS (using systemd).

Fixed
~~~~~

- Downgrade Travis CI Docker version by force to resolve build error.
- Remove unsupported Debian version from Galaxy metadata.

3.0.1 (2016-12-10)
------------------

Fixed
~~~~~

-  (`#9 <https://github.com/devops-coop/ansible-minecraft/isues/9>`_) Fixed ``RuntimeError`` regression when building ACL files.

3.0.0 (2016-07-15)
------------------

Added
~~~~~

-  (`#5 <https://github.com/devops-coop/ansible-minecraft/pull/5>`_) Manage ``server.properties`` by setting ``minecraft_server_properties`` (Mark Côté).
-  (`#6 <https://github.com/devops-coop/ansible-minecraft/issues/6>`_) Hooks: Include additional tasks at specific points during execution.

Changed
~~~~~~~

-  Install latest major release of Minecraft by default.

Fixed
~~~~~

-  (`#4 <https://github.com/devops-coop/ansible-minecraft/issues/4>`_) Improve build documentation.

2.2.0 (2016-05-30)
------------------

Added
~~~~~

-  It is now possible to install the latest major release of Minecraft using ``minecraft_version: latest``.

Deprecated
~~~~~~~~~~

-  The hard-coded default version (currently ``1.9``) will be replaced with ``latest`` in the next major version.

Fixed
~~~~~

-  Only generate ACL JSON files if the variables (e.g., ``minecraft_ops``) are non-empty.
-  Resolve deprecation warnings.

2.1.1 (2016-03-08)
------------------

-  Notify Galaxy on successful build.

2.1.0 (2016-03-08)
------------------

Added
~~~~~

-  Integrate Travis CI for automated integration testing.

Changed
~~~~~~~

-  Replace Vagrant test environments with Docker test harness.

Fixed
~~~~~

-  Correct minimum Ansible version (requires Ansible 1.8+).

2.0.0 (2016-03-01)
------------------

Added
~~~~~

-  Add `AUTHORS <AUTHORS.rst>`_ file.

Changed
~~~~~~~

-  Install latest 1.9 release by default.
-  Change default process supervisor (``minecraft_process_control``) from ``supervisor`` to ``systemd``.

1.4.0 (2016-01-23)
------------------

Changed
-------

-  Replace ACL script with Ansible module.

1.3.1 (2015-11-29)
------------------

Fixed
-----

-  Fix table rendering on Ansible Galaxy.

1.3.0 (2015-11-29)
------------------

Added
-----

-  Add Vagrant integration test suite.

Deprecated
----------

-  The default process supervisor (``minecraft_process_control``) will change from ``supervisor`` to ``systemd`` in the next major version.

Fixed
-----

-  Configure Supervisor to run Java with absolute path (``/usr/bin/java``).
-  Add RHEL/CentOS to supported platforms on Ansible Galaxy.

1.2.0 (2015-11-26)
------------------

Added
-----

-  Add support for CentOS 7.

Fixed
-----

-  Create ``/run/minecraft`` directory properly using ``systemd-tmpfiles``
-  Fix socket permissions for systemd < 214.
-  Do not update apt cache.
-  Download server before starting the service for the first time.

1.1.0 (2015-11-24)
------------------

Added
-----

-  Support systemd.
-  Add Debian 8 test environment.

Changed
-------

-  Bump default server version to ``1.8.8``.

1.0.0 (2015-11-23)
------------------

Initial release
