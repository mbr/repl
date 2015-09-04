import click

from . import repl as repl_mod


@click.command(
    help='Starts a print-execute-print-loop by running the '
    'supplied with input read from the terminal.',
    epilog='Arguments can be given inline by using {}: "repl foo {} --bar" '
    'will run replacing the {} with entered arguments. To suppress '
    'this behavior completely, "--sub=" can be used.')
@click.argument('command', nargs=-1)
@click.option('--color/--no-color',
              default=True,
              help='Enable/disable colorized prompt (enabled by default).')
@click.option('--external/--no-external',
              default=True,
              help='Enable/disable external command execution using ! '
              '(enabled by default).')
@click.option('--sub',
              default='{}',
              help='Placeholder for argument substitution')
@click.option('--repl-type',
              help='Force specific REPL type (default: autodetect)')
@click.option('--external/--no-external')
@click.option('--prompt', help='Override prompt')
def repl(repl_type, command, **kwargs):
    if repl_type:
        rt = repl_mod.available_repls[repl_type]
    else:
        rt = repl_mod.REPL

        for rc in repl_mod.available_repls.values():
            if rc.detect(command):
                rt = rc
                break

    r = rt(command=command, **kwargs)
    if not r.has_readline:
        click.secho(
            'No readline support. Tab completion and history unavailable',
            fg='yellow',
            err=True)

    r.run()
