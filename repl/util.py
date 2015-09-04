import os
import sys


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
    sys.stdout.write("\x1b]2;{}\x07".format(title))

# Python2/3 compatibility
if sys.version_info.major <= 2:
    inp = raw_input
else:
    inp = input
