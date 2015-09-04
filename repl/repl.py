import atexit
import os
import shlex
import subprocess
import sys

import click

from .util import fcomplete, set_title, inp, replace_slice


class REPL(object):
    def __init__(self, color, prompt, sub, command, external):
        self.color_enabled = color
        self.prompt_string = prompt
        self.cmd_sub_str = sub
        self.command = command
        self.enable_external = external

        self.setup_readline()

    def setup_readline(self):
        try:
            import readline
        except ImportError:
            self.has_readline = False
        else:
            # determine history file name
            if not self.command:
                histname = 'history'
            else:
                histname = 'history-' + self.command[0].replace(os.sep, '_')
            histfile = os.path.join(click.get_app_dir('repl'), histname)

            # read old history, of present
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass

            atexit.register(readline.write_history_file, histfile)
            readline.parse_and_bind('tab: complete')
            readline.set_completer_delims(' \t\n')
            readline.set_completer(fcomplete)
            self.has_readline = True

        # got readline support
        return self.has_readline

    def colorize(self, sequence, text, end="00"):
        # see: https://stackoverflow.com/questions/9468435/
        # look-how-to-fix-column-calculation-in-python-readline-if-use-color-prompt
        #
        # and: http://bugs.python.org/issue12972'
        #      http://wiki.hackzine.org/development/misc/readline-color-prompt.html

        rl_start = rl_end = ''

        if self.has_readline:
            rl_start = '\001'
            rl_end = '\002'

        return (rl_start + "\033[" + sequence + "m" + rl_end + text + rl_start
                + "\033[" + end + "m" + rl_end)

    @property
    def prompt(self):
        if self.prompt_string is not None:
            return self.prompt_string

        if not self.color_enabled:
            return ' '.join(self.command) + '>> '

        color = '34'
        sub_color = '37'

        prompt_cmd = [
            self.colorize('1;' + color, part) if part != self.cmd_sub_str else
            self.colorize('0;' + sub_color, u'\u2026') for part in self.command
        ]
        return ' '.join(prompt_cmd) + self.colorize('0;' + color, '>> ')

    @property
    def title(self):
        return '[{}] {}>>'.format(
            os.path.split(os.path.abspath('.'))[-1], ' '.join(self.command))

    def run(self):
        while True:
            set_title(self.title)

            try:
                line = inp(self.prompt).lstrip()
                if not self.enable_external and line.startswith('!'):
                    cmd_args = shlex.split(line[1:])
                    subprocess.call(cmd_args)
                    continue
                uargs = shlex.split(line)
            except EOFError:
                print()
                sys.exit(0)
            except ValueError as e:
                print(e)
                continue

            # substitute values
            cmd = replace_slice(self.cmd_sub_str, uargs, self.command,
                                append=True)

            set_title(' '.join(cmd))
            subprocess.call(cmd)


class GitREPL(REPL):
    @classmethod
    def detect(self, command):
        return ['git'] == [c for c in command if not c.startswith('-')]


available_repls = {'git': GitREPL}
