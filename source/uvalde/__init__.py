import click

from uvalde.import_command import import_
from uvalde.list_commands import list_all, list_nvrs, list_repos
from uvalde.move_command import move


@click.group()
def main():
    """Yum repository management tool."""


@click.group('list')
def list_group():
    """List subcommands."""


list_group.add_command(list_all)
list_group.add_command(list_nvrs)
list_group.add_command(list_repos)
main.add_command(list_group)

main.add_command(import_)
main.add_command(move)
