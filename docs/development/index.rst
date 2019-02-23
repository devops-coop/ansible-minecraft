Development
=====================

This section shoud be descripe how the development process *(coding, testing, releasing and publishing)* works.

.. toctree::
   :maxdepth: 2

   building
   testing
   public-services


.. role:: red

Branch Modell
------------------------------------------

As Branchmodel we use a mix of `Gitflow <https://datasift.github.io/gitflow/IntroducingGitFlow.html>`_ and `pull-requests <https://help.github.com/articles/about-pull-requests/>`_.
Gitflow is used for the Release Process, the ``master`` branch present the latest Published Release.
PullRequests are used for integrate external changes and ``feature`` branches into the ``develop`` branch.

| The ``develop`` branch contains the latest unrelesed version from the role, mostly stable ;)
| New features will be develop in feature branches like ``feature/integrate-cuberite``, :red:`it`s not recomendet to use this on PRODUCTION!!!`.
| The ``master`` present the latest published release.

For the `Continuous Integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ we use `Travis CI <https://travis-ci.org>`_ |Travis CI build status| as service.


.. include:: ../links.rst
