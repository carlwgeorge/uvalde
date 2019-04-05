import click

from uvalde.import_command import import_
from uvalde.config_commands import config_show
from uvalde.list_commands import list_all, list_nvrs, list_repos
from uvalde.move_command import move
from uvalde.remove_command import remove


@click.group()
def main():
    """Yum repository management tool."""


@click.group('config')
def config_group():
    """Config subcommands."""


@click.group('list')
def list_group():
    """List subcommands."""


config_group.add_command(config_show)
main.add_command(config_group)

list_group.add_command(list_all)
list_group.add_command(list_nvrs)
list_group.add_command(list_repos)
main.add_command(list_group)

main.add_command(import_)
main.add_command(move)
main.add_command(remove)
