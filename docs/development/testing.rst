Testing
==================================
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


Testing with Molecule
-------------------------------------------------------------------

The Tests are impemented with `Molecule <https://molecule.readthedocs.io>`_

.. code-block:: shell

  molecule test -s spigot

Molecule Tips
`````````````````````````````````````````````````````````````````````

**Starting the Containers**
.. code-block:: shell

  molecule create


.. code-block:: shell

  molecule converge

  docker exec -t -i centos7 /bin/bash

  verify       Run automated tests against instances.

Testing with Vagrant
-------------------------------------------------------------------

This role includes a Vagrantfile used with a Docker-based test harness that approximates the Travis CI setup for integration testing. Using Vagrant allows all contributors to test on the same platform and avoid false test failures due to untested or incompatible docker versions.

1. Install `Vagrant <https://www.vagrantup.com/>`__ and `VirtualBox <https://www.virtualbox.org/>`__.
1.1 Accept the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`__ with setting a Environment Property like: ``export mc_accept_eula=true && vagrant up``

2. Run ``vagrant up`` from the same directory as the Vagrantfile in this repository.

Now you can Connect with your Game again the Testserver on ``localhost:25565`` and test your server.

3. for manual lookups you can connect over SSH into the VM with: ``vagrant ssh``

.. include:: ../links.rst
