Developer Guide
$$$$$$$$$$$$$$$

This section contains everything that a StrictDoc developer/contributor should
know to get the job done.

StrictDoc is based on Python and maintained as any other Python package on
GitHub: with linting, tests, and hopefully enough best practice put into the
codebase.

The instructions are conventions described below are the summary of what is
considered to be the currently preferred development style for StrictDoc.
These rules have been relatively stable for quite a while but any rule can still
be changed if a better development practice is found.

Any feedback on this development guide is appreciated.

.. _DEVGUIDE_GETTING_STARTED:

Getting started
===============

Installing StrictDoc from GitHub (developer mode)
-------------------------------------------------

**Note:** Use this way of installing StrictDoc only if you want to make changes
in StrictDoc's source code. Otherwise, install StrictDoc as a normal Pip package by running ``pip install strictdoc``.

.. code-block::

    git clone https://github.com/strictdoc-project/strictdoc.git && cd strictdoc
    pip install .[development]
    python3 strictdoc/cli/main.py

Invoke for development tasks
============================

All development tasks are managed using
`Invoke <https://www.pyinvoke.org/>`_ in the ``tasks.py`` file. On macOS and
Linux, all tasks run in dedicated virtual environments. On Windows, invoke uses
the parent pip environment, which can be a system environment or a user's virtual
environment.

Make sure to familiarize yourself with the available developer tasks by running:

.. code-block:: bash

    invoke --list

.. _DEVGUIDE_PYTHON_CODE:

Python code
===========

- The version of Python is set to be as low as possible given some constraints
  of StrictDoc's dependencies. Ideally, the lowest Python version should only be
  raised when it is consistently deprecated by major software platforms like
  Ubuntu or GitHub Actions.

- All developer tasks are collected in the ``tasks.py`` which is run by Invoke
  tool. Run the ``invoke --list`` command to see the list of available commands.

- Formatting is governed by ``black`` which reformats the code automatically
  when the ``invoke check`` command is run.

  - If a string literal gets too long, it should be split into a multiline
    literal with each line being a meaningful word or subsentence.

- If a contribution includes changes in StrictDoc's code, at least the
  integration-level tests should be added to the ``tests/integration``. If the
  contributed code needs a fine-grained control over the added behavior, adding
  both unit and integration tests is preferred. The only exception where a
  contribution can contain no tests is "code climate" which is work which
  introduces changes in code but no change to the functionality.

.. _DEVGUIDE_GIT_WORKFLOW:

Git workflow
============

- The preferred Git workflow is "1 commit per 1 PR". If the work truly deserves
  a sequence of commits, each commit shall be self-contained and pass all checks
  from the ``invoke check`` command. The preferred approach: split the work into
  several independent Pull Requests to simplify the work of the reviewer.

- The branch should be always rebased against the main branch. The
  ``git fetch && git rebase origin/main`` is preferred over
  ``git fetch && git merge main``.

- The Git commit message should follow the format:

.. code-block::

    context: description

where the context can be a major feature being added or a folder. A form of  ``context: subcontext: description`` is also an option. Typical examples:

``docs: fix links to the grammar.py``

``reqif: native: export/import roundtrip for multiline requirement fields``

``backend/dsl: switch to dynamic fields, with validation``

``Poetry: add filecheck as a dependency``

- Use comma-separated contexts, if the committed work is dedicated to more than one topic. Example:

.. code-block::

    server, UI: update to new requirement styles

- When a contribution is simply an improvement of existing code without a change
  in the functionality, the commit should be named: ``Code climate: description``. Example:

.. code-block::

    Code climate: fix all remaining major Pylint warnings

Frontend development
====================

The shortest path to run the server when the StrictDoc's source code is cloned:

.. code-block:: bash

    invoke server

Running integration tests
=========================

The integration tests are run using Invoke:

.. code-block:: bash

    invoke test-integration

The ``--focus`` parameter can be used to run only selected tests that match a given substring. This helps to avoid running all tests all the time.

.. code-block:: bash

    invoke test-integration --focus <keyword>


Documentation
=============

- Every change in the functionality or the infrastructure should be documented.
- Every line of documentation shall be no longer than 80 characters. StrictDoc's
  own documentation has a few exceptions, however, the latest preference is
  given to 80 characters per line. Unfortunately, until there is automatic
  support for mixed SDoc/RST content, all long lines shall be edited and
  split by a contributor manually.
- The ``invoke docs`` task should be used for re-generating documentation on a
  developer machine.

Conventions
===========

- ``snake_case`` everywhere, no ``kebab-case``.

  - This rule applies everywhere where applicable: file and folder names, HTML attributes.
  - Exception: HTML data-attributes and ``testid`` identifiers.
