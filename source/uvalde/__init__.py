import click

from uvalde.import_command import import_
from uvalde.config_commands import config_show
from uvalde.list_command import list_
from uvalde.move_command import move
from uvalde.remove_command import remove


@click.group()
def main():
    """Yum repository management tool."""


@click.group('config')
def config_group():
    """Config subcommands."""


config_group.add_command(config_show)
main.add_command(config_group)

main.add_command(import_)
main.add_command(list_)
main.add_command(move)
main.add_command(remove)
