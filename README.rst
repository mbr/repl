repl
====

.. image:: repl-demo.gif

Runs a command in a `REPL <https://en.wikipedia.org/wiki/Read-eval-
print_loop>`_. It comes in very handy when dealing with applications that do
not ship with a REPL, but could benefit greatly from one (such as git_).

Tab completion is available and completes filenames.

Real productivity
-----------------

Set an alias in your shell's start-up file:

    alias rg="repl git"

Instead of typing ``git ...``, type ``rg`` once. You'll never go back.


Installation
------------

Requires nothing but Python installed. No extra dependencies, just stdlib. Drop
this right into your ``$PATH``, ``chmod +x`` and you are good to go.


.. _git: https://git-scm.com

Credits
-------

Idea stolen from https://github.com/defunkt/repl, which unfortunately is
unmaintained. Originally rewritten because I had issues with stdin/stdout; now
it boasts a few extra features (and does not require ruby)
