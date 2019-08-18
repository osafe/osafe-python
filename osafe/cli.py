#!/usr/bin/env python3

import click

from .editor import Editor
from .config import Config


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(edit)


@main.command()
def edit():
    Editor().start()


@main.command()
@click.option('-t', '--timeout', type=int, help="Timeout for the editor in minutes. Use '0' for no timeout. Defaults to '5'")
def config(timeout):
    if timeout is None:
        print(Config.get().content)
    else:
        Config.get().write(
            timeout=timeout,
        )


if __name__ == '__main__':
    main()
