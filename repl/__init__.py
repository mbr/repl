#!/usr/bin/python -u

import argparse
import shlex
import sys
import subprocess
import os
import warnings

# Python2/3 compatibility
if sys.version_info.major <= 2:
    inp = raw_input
else:
    inp = input


def fcomplete(text, state):
    text = os.path.expanduser(text)
    head, tail = os.path.split(text)

    search_dir = os.path.join('.', head)
    candidates = [s for s in os.listdir(search_dir) if s.startswith(tail)]

    if state >= len(candidates):
        return None

    if len(candidates) == 1:
        fn = os.path.join(head, candidates[0])
        if not os.path.isdir(fn):
            return fn + ' '
        return fn + '/'

    return os.path.join(head, candidates[state])


def colorize(sequence, text, end="00", rlp=True):
    # see: https://stackoverflow.com/questions/9468435/
    # look-how-to-fix-column-calculation-in-python-readline-if-use-color-prompt
    #
    # and: http://bugs.python.org/issue12972'
    #      http://wiki.hackzine.org/development/misc/readline-color-prompt.html

    rl_start = rl_end = ''

    if rlp:
        rl_start = '\001'
        rl_end = '\002'

    return (rl_start + "\033[" + sequence + "m" + rl_end + text + rl_start +
            "\033[" + end + "m" + rl_end)


def replace_slice(placeholder, replacement, l, append=False):
    rv = []
    found = False
    for elem in l:
        if elem == placeholder:
            rv.extend(replacement)
            found = True
            continue
        rv.append(elem)

    if not found and append:
        rv.extend(replacement)

    return rv


def set_title(title):
    sys.stdout.write("\x1b]2;{}\x07".format(title))


def main():
    rlp = False
    try:
        import readline
        import xdg.BaseDirectory
    except ImportError as e:
        warnings.warn('{}. History and tab completion disabled.'.format(e))
        pass  # no readline or xdg support
    else:
        import atexit

        conf = xdg.BaseDirectory.save_config_path('repl')
        histfile = os.path.join(conf, 'history')

        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

        atexit.register(readline.write_history_file, histfile)
        readline.parse_and_bind('tab: complete')
        readline.set_completer_delims(' \t\n')
        readline.set_completer(fcomplete)
        rlp = True

    parser = argparse.ArgumentParser(
        description=
        'Starts a print-execute-print-loop by running the supplied '
        'with input read from the terminal.',
        epilog='Arguments can be given inline by using {}: "repl foo {} --bar"'
        '\n\nwill run replacing the {} with entered arguments. To suppress '
        'this behavior completely, "--sub=" can be used.')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    parser.add_argument('--no-color',
                        default=False,
                        action='store_true',
                        help='do not colorized prompt.')
    parser.add_argument('--prompt', help='override prompt')
    parser.add_argument(
        '--no-external',
        action='store_true',
        default=False,
        help='forbid execution of external commands (using a prefix of \'!\')')
    parser.add_argument('--sub', default='{}', help='argument to replace')
    args = parser.parse_args()

    if args.prompt:
        prompt = args.prompt
    elif args.no_color:
        prompt = ' '.join(args.command) + '>> '
    else:
        color = '34'
        sub_color = '37'

        prompt_cmd = [
            colorize('1;' + color, part,
                     rlp=rlp)
            if part != args.sub else colorize('0;' + sub_color, u'\u2026',
                                              rlp=rlp) for part in args.command
        ]
        prompt = ' '.join(prompt_cmd) + colorize('0;' + color, '>> ', rlp=rlp)
        prompt_name = ('[{}] {}>>'.format(
            os.path.split(os.path.abspath('.'))[-1], ' '.join(args.command)))

    while True:
        set_title(prompt_name)
        try:
            line = inp(prompt).lstrip()
            if not args.no_external and line.startswith('!'):
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
        cmd = replace_slice(args.sub, uargs, args.command, append=True)

        set_title(' '.join(cmd))
        subprocess.call(cmd)
