########
not-grep
########

.. image:: https://img.shields.io/pypi/v/not-grep.svg
   :target: https://pypi.python.org/pypi/not-grep
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/not-grep.svg
   :target: https://pypi.python.org/pypi/not-grep
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code_style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black

.. image:: https://readthedocs.org/projects/not-grep/badge/
   :target: https://not-grep.readthedocs.io
   :alt: Documentation Status

.. important::

    This project is a work in progress and is not yet ready for use.

``not-grep`` is kind of like grep, but not quite the same.

WAT?
====

If you have ever found the need to inspect a file for particular patterns,
you probably used ``grep``.

.. code-block:: bash

    grep FooClassName file.py

If you needed to do that for a lot of files, you might have combined it with ``find``.

.. code-block:: bash

    find . -type f -name "*.py" -exec grep -n FooClassName {} /dev/null \;

This works great for one-off checks
but less great if you need to do those checks repeatedly,
if you need to do lots of such checks,
if you need to do those checks somewhere that you don't have access to ``grep``,
or if you need to do things that ``grep`` cannot do.

Not Grep?
=========

``not-grep`` is designed for static use, not ad-hoc use.
For example, as part of a continuous integration test suite.
This is why it gets its configuration from a config file, not the CLI.
Because of this, the ``not-grep`` CLI is very simple:
the only things you can specify are the config file and verbosity.

.. code-block:: bash

    not-grep --config config.toml -vv

Inside the config file, things start to get interesting.

``not-grep`` is built around checker plugins.
Each plugin takes a map as input:
the file glob pattern for the files you want to check
and a value that tells the plugin what to do with that file.

The config file is a collection of TOML tables.
The table name identifies the plugin
and the table members are the input to that plugin.

.. code-block:: toml

    # The "present" checker will error unless the specified value is present.
    [present]
    "src/**/*.py" = "__all__"

    # The "not-present" checker will error if the specified value is present.
    [not-present]
    "src/**/*.py" = "FooClassName"


The output shows you, for each plugin,
whether each matched file met or failed the plugin requirements.
In lower verbosity levels, ``not-grep`` only shows failed checks.

.. code-block:: bash

    $ not-grep --config config.toml -vv
    ================Running present checks================
    -----------Checking src/**/*.py for pattern-----------
    __all__
    ******************************************************
    src/foo/__init__.py.............................. PASS
    src/foo/bar.py................................... FAIL

    ==============Running not-present checks==============
    -----------Checking src/**/*.py for pattern-----------
    FooClassName
    ******************************************************
    src/foo/__init__.py.............................. PASS
    src/foo/bar.py................................... PASS

Awesome! Can I use it in GitHub Actions?
========================================

Yes. Yes you can.

.. code-block:: yaml

    - uses: mattsb42/not-grep@master
      with:
        # If you don't set config-file the action uses ".github/not-grep.toml".
        config-file: ./github/config/check-things.toml
        # If you don't set debug, passing checks will be hidden.
        debug: true
