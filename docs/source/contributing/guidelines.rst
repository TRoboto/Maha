=======================
Contribution Guidelines
=======================

For first-time contributors
---------------------------
#. Install git:

   For instructions see https://git-scm.com/.


#. Fork the project. Go to https://github.com/TRoboto/Maha and
   click the "fork" button to create a copy of the project for you to work on. You will
   need a GitHub account. This will allow you to make a "Pull Request" (PR)
   to the main repo later on.

#. Clone your fork to your local computer:

   .. code-block:: shell

      git clone https://github.com/<your-username>/maha.git

   GitHub will provide both a SSH (``git@github.com:<your-username>/maha.git``) and
   HTTPS (``https://github.com/<your-username>/maha.git``) URL for cloning.
   You can use SSH if you have SSH keys setup.

   .. WARNING::

      Do not clone the TRoboto/Maha repository. You must clone your own
      fork.

#.  Change the directory to enter the project folder:

    .. code-block:: shell

       cd maha

#. Add the upstream repository as a remote:

   .. code-block:: shell

      git remote add upstream https://github.com/TRoboto/Maha.git

#. Now, ``git remote -v`` should show two remote repositories named:

   - ``origin``, your forked repository
   - ``upstream`` the TRoboto repository

#. Install Maha:

   - We recommend using `Poetry <https://python-poetry.org>`__ to manage your
     developer installation of Maha. Poetry is a tool for dependency
     management and packaging in Python. It allows you to declare the libraries
     your project depends on, and it will manage (install / update) them
     for you. In addition, Poetry provides a simple interface for
     managing virtual environments.

     If you choose to use Poetry as well, follow `Poetry's installation
     guidelines <https://python-poetry.org/docs/master/#installation>`__
     to install it on your system, then run ``poetry install`` from
     your cloned repository. Poetry will then install Maha, as well
     as create and enter a virtual environment. You can always re-enter
     that environment by running ``poetry shell``.

   - In case you decided against Poetry, you can install Maha via pip
     by running ``python3 -m pip install .``. Note that due to our
     development infrastructure being based on Poetry, we currently
     do not support editable installs via ``pip``, so you will have
     to re-run this command every time you make changes to the source
     code.

   .. note::

      The following steps assume that you chose to install and work with
      Poetry.

#. Install Pre-Commit:

   .. code-block:: shell

      poetry run pre-commit install

   This will ensure during development that each of your commits is properly
   formatted against our linter and formatters, ``black`` and ``isort``

You are now ready to work on Maha!

Develop your contribution
-------------------------

#. Checkout your local repository's main branch and pull the latest
   changes from TRoboto/main, ``upstream``, into your local repository:

   .. code-block:: shell

      git checkout main
      git pull --rebase upstream main

#. Create a branch for the changes you want to work on rather than working
   off of your local main branch:

   .. code-block:: shell

      git checkout -b <new branch name> upstream/main

   This ensures you can easily update your local repository's main with the
   first step and switch branches to work on multiple features.

#. Write some awesome code!

   You're ready to make changes in your local repository's branch.
   You can add local files you've changed within the current directory with
   ``git add .``, or add specific files with

   .. code-block:: shell

      git add <file/directory>

   and commit these changes to your local history with ``git commit``. If you
   have installed pre-commit, your commit will succeed only if none of the
   hooks fail.

   .. tip::

      When crafting commit messages, it is highly recommended that
      you adhere to `these guidelines <https://www.conventionalcommits.org/en/v1.0.0/>`_.

#. Add new or update existing tests.

   Depending on your changes, you may need to update or add new tests. For new
   features, it is required that you include tests with your PR.


#. Update docstrings and documentation:

   Update the docstrings (the text in triple quotation marks) of any functions
   or classes you change and include them with any new functions you add.
   See the :doc:`documentation guide <docstring>` for more information about how we
   prefer our code to be documented. The content of the docstrings will be
   rendered in the :doc:`reference manual <../reference>`.

As far as development on your local machine goes, these are the main steps you
should follow.

Polishing Changes and Submitting a Pull Request
-----------------------------------------------

As soon as you are ready to share your local changes with the community
so that they can be discussed, go through the following steps to open a
pull request.

.. note::

   You do not need to have everything (code/documentation/tests) complete
   to open a pull request (PR). If the PR is still under development, please
   mark it as a draft. Other developers will still be able to review the
   changes, discuss yet-to-be-implemented changes, and offer advice; however,
   the more complete your PR, the quicker it will be merged.

#. Update your fork on GitHub to reflect your local changes:

   .. code-block:: shell

      git push -u origin <branch name>

   Doing so creates a new branch on your remote fork, ``origin``, with the
   contents of your local repository on GitHub. In subsequent pushes, this
   local branch will track the branch ``origin`` and ``git push`` is enough.

#. Make sure all of your changes don't break the tests:

   .. code-block:: shell

      poetry run tox

   Doing so runs all checks and testscreates a new branch on your remote fork, ``origin``,
   with the contents of your local repository on GitHub. In subsequent pushes, this
   local branch will track the branch ``origin`` and ``git push`` is enough.

#. Make a pull request (PR) on GitHub.

   In order to make Other developers aware of your changes,
   you can make a PR to the TRoboto/Maha repository from your fork.

   Please make sure you follow the PR template (this is the default
   text you are shown when first opening the 'New Pull Request' page).


Your changes are eligible to be merged if:

#. there are no merge conflicts
#. the tests in our pipeline pass
#. at least two (three for more complex changes) developers approve the changes

You can check for merge conflicts between the current upstream/main and
your branch by executing ``git pull upstream main`` locally. If this
generates any merge conflicts, you need to resolve them and push an
updated version of the branch to your fork of the repository.

Our pipeline consists of a series of different tests that ensure
that Maha still works as intended and that the code you added
sticks to our coding conventions.

- **Code style**: We use the code style imposed
  by `Black <https://black.readthedocs.io/en/stable/>`_, `isort <https://pycqa.github.io/isort/>`_
  and `mypy <https://mypy.readthedocs.io/en/stable/>`_. The GitHub pipeline
  makes sure that the (Python) files changed in your pull request
  also adhere to this code style. If this step of the pipeline fails,
  fix your code formatting automatically by running ``tox`` and then fix the problems
  manually that were detected by ``mypy``.

- **Tests**: The pipeline runs Maha's test suite on different operating systems
  (the latest versions of Ubuntu, MacOS, and Windows) for different versions of Python.
  The test suite consists of two different kinds of tests: integration tests
  and doctests. You can run them locally by executing ``tox`` from the
  root directory of your cloned fork.

- **Documentation**: We also build a version of the documentation corresponding
  to your pull request. Make sure not to introduce any Sphinx errors, and have
  a look at the built HTML files to see whether the formatting of the documentation
  you added looks as you intended. You can build the documentation locally
  by running ``make html`` from the ``docs`` directory.

Finally, if the pipeline passes and you are satisfied with your changes: wait for
feedback and iterate over any requested changes. You will likely be asked to
edit or modify your PR in one way or another during this process. This is not
an indictment of your work, but rather a strong signal that the community
wants to merge your changes! Once approved, your changes may be merged!

Further useful guidelines
=========================

#. When submitting a PR, please mention explicitly if it includes breaking changes.

#. When submitting a PR, make sure that your proposed changes are as general as
   possible, and ready to be taken advantage of by all of Maha's users. In
   particular, leave out any machine-specific configurations, or any personal
   information it may contain.

#. If you are a maintainer, please label issues and PRs appropriately and
   frequently.

#. When opening a new issue, if there are old issues that are related, add a link
   to them in your new issue (even if the old ones are closed).

#. When submitting a code review, it is highly recommended that you adhere to
   `these general guidelines <https://conventionalcomments.org/>`_.

#. If you find stale or inactive issues that seem to be irrelevant, please post
   a comment saying 'This issue should be closed', and a developer will take a look.

#. Please do as much as possible to keep issues, PRs, and development in
   general as tidy as possible.


You can find examples for the ``docs`` in several places:
the :doc:`Overview <../overview>`, and :doc:`Reference Manual <../reference>`.

**Thank you for contributing!**
