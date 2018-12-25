Development
=====================

.. role:: red


| The ``develop`` branch contains the latest unrelesed version from the role, mostly stable ;)
| New features will be develop in feature branches like ``feature/integrate-cuberite``, :red:`it`s not recomendet to use this on PRODUCTION!!!`.

For the `Continuous Integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ we use `Travis CI <https://travis-ci.org>`_ |Travis CI build status| as service.


Building
--------------------

As build script we use `Tox <https://tox.readthedocs.io/en/latest/config.html>`_, so it`s easy to execute the different kind of build commands like, generate docs or execute tests.

.. code-block:: shell

  tox -e spigot

**Possible Tox Envs**

+-------------+--------------------------------------------------------------------------------------------------------------------------------+
| env         | Description                                                                                                                    |
+-------------+--------------------------------------------------------------------------------------------------------------------------------+
| ``docs``    | generates the sphinx documentation page (generated to ``.tox/docs/tmp/html/``)                                                 |
+-------------+--------------------------------------------------------------------------------------------------------------------------------+
| ``default`` | Execute an Molecule tests for the classic vanilla Minecraft server (Tested ``CentOS7``,``Ubuntu1604``,``Ubuntu18``,``Debian``) |
+-------------+--------------------------------------------------------------------------------------------------------------------------------+
| ``spigot``  | Execute the Molecule tests for a spigot server.                                                                                |
+-------------+--------------------------------------------------------------------------------------------------------------------------------+


Versioning
************************************

This project follows `semantic versioning <http://semver.org/>`_.

In the context of semantic versioning, consider the role contract to be defined by the role variables.

-  Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
-  Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
-  Bug fixes will increase the **patch** version.


Releasing
************************************

- `bumpversion <https://github.com/peritus/bumpversion/blob/master/README.rst>`_

a simple version update can be manual executed with:

.. code-block:: shell

    bumpversion minor

the updateable files are listed at ``.bumpversion.cfg`` at the project root directory.

Testing
--------------------

The Tests are impemented with `Molecule <https://molecule.readthedocs.io>`_

.. code-block:: shell

  molecule test -s spigot

Molecule Tips
*******************************

**Starting the Containers**
.. code-block:: shell

  molecule create


.. code-block:: shell

  molecule converge

  docker exec -t -i centos7 /bin/bash

  verify       Run automated tests against instances.

.. |Travis CI build status| image:: https://travis-ci.org/nolte/ansible-minecraft.svg?branch=develop
    :target: https://travis-ci.org/nolte/ansible-minecraft
