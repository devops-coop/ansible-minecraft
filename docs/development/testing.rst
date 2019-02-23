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

| For the development and debugging it is easyer and faster to execute the Molecule sequenzes step by step.
| First you must start the container with ``molecule create``, after the containers started, you can execute the Role/Playbook ``molecule converge``.
| Now, when all the steps are finished, you can execute the Integration Tests with ``molecule verify``

.. note::

  For Debugging the role take a look into the container with ``docker exec -t -i centos7 /bin/bash``


Testing with Vagrant
-------------------------------------------------------------------

| This role includes a Vagrantfile used for `Exploratory testing <https://en.wikipedia.org/wiki/Exploratory_testing>`_.
| If you want to use this vagrant machine follow this steps:

| 1. Install `Vagrant <https://www.vagrantup.com/>`_ and `VirtualBox <https://www.virtualbox.org/>`_.
| 1.1. Accept the `Minecraft EULA <https://account.mojang.com/documents/minecraft_eula>`_ with setting a Environment Property like: ``export mc_accept_eula=true``
| 2. Run ``vagrant up`` from the same directory as the Vagrantfile in this repository.

.. note::
  Now, you can start the game and conntecting again our server e.g. ``localhost:25565`` and test the changes.

| 3. for manual lookups you can connect over SSH into the VM with: ``vagrant ssh``

.. note::
  If the Vagrant box allways exists, you can reexecute the Playbook with ``vagrant rsync && vagrant provision``

.. include:: ../links.rst
