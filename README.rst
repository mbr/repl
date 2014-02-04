repl
====

Disclaimer: 5 minute hack.

Runs a command in a `REPL
<https://en.wikipedia.org/wiki/Read-eval-print_loop>`_ loop. My personal use
case is this::

   % repl git
   git>> init .Initialized empty Git repository in ...
   git>> add README.rst
   git>> commit -m 'Initial commit.'
   [master (root-commit) d18bb26] Initial commit.
    1 file changed, 8 insertions(+)
    create mode 100644 README.rst
   git>> (CTRL+D)
   %

Idea stolen from https://github.com/defunkt/repl, which unfortunately is
unmaintained and does something funky with stdin/stdin (which may be a ruby
issue), causing things to break inside SublimeREPL.
