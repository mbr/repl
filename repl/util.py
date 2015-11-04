import fcntl
import os
import re
import struct
import sys
import termios


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


def fcomplete(text, state):
    """Readline completion function: Filenames"""

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


def set_title(title):
    """Set the title of the terminal."""
    sys.stdout.write("\x1b]2;{}\x07".format(title.encode('utf8')))

# Python2/3 compatibility
if sys.version_info.major <= 2:
    inp = raw_input
else:
    inp = input


def get_terminal_size(fileno=None):
    if fileno is None:
        fileno = sys.stdout.fileno()

    buf = struct.pack('HHHH', 0, 0, 0, 0)
    res = fcntl.ioctl(fileno, termios.TIOCGWINSZ, buf)
    h, w, _, _ = struct.unpack('HHHH', res)

    return (w, h)


_ANSI_ESCAPE_EXP = re.compile(r'\x1b[^m]*m')


def strip_control(s):
    return _ANSI_ESCAPE_EXP.sub('', s)
