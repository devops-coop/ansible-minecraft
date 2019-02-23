Building
=========================================================

As build script we use `Tox <https://tox.readthedocs.io/en/latest/config.html>`_, so it`s easy to execute the different kind of build commands like, generate docs or execute tests.

.. code-block:: shell

  tox -e spigot

**Possible Tox Envs**

+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| env         | Description                                                                                                                                   |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``docs``    | generates the sphinx documentation page (generated to ``.tox/docs/tmp/html/``)                                                                |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``default`` | Execute an Molecule tests for the classic vanilla Minecraft server (Tested ``CentOS7``, ``Ubuntu1604``, ``Ubuntu18``, ``DebianJessie``)       |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| ``spigot``  | Execute the Molecule tests for a spigot server.                                                                                               |
+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+


Versioning
----------------------------------------------------------------------

This project follows `semantic versioning <http://semver.org/>`_.

In the context of semantic versioning, consider the role contract to be defined by the role variables.

-  Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
-  Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
-  Bug fixes will increase the **patch** version.


Handling Version
``````````````````````````````````````````````````````````````````````

| For handle the version number in the different files we use the `bumpversion <https://github.com/peritus/bumpversion/blob/master/README.rst>`_ tool.
| The updateable files are listed at ``.bumpversion.cfg`` placed in the project root directory.

Update project minor version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Call bumpversion on the commandline like:

.. code-block:: shell

    bumpversion minor

for update the **minor** version of this project.


Releasing
----------------------------------------------------------------------
