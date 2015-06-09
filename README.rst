repl
====

.. image:: repl-demo.gif

Runs a command in a `REPL <https://en.wikipedia.org/wiki/Read-eval-
print_loop>`_. My personal use case is this::

   % repl git
   git>> init .
   Initialized empty Git repository in ...
   git>> add README.rst
   git>> commit -m 'Initial commit.'
   [master (root-commit) d18bb26] Initial commit.
    1 file changed, 8 insertions(+)
    create mode 100644 README.rst
   git>> (CTRL+D)
   %

Tab completion is available, but only completes filenames.

Idea stolen from https://github.com/defunkt/repl, which unfortunately is
unmaintained. Rewritten because I had issues with stdin/stdout.
