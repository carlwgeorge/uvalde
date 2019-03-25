import click

from uvalde.commands.import_ import import_
from uvalde.commands.list_all import list_all
from uvalde.commands.list_nvrs import list_nvrs
from uvalde.commands.list_repos import list_repos


@click.group()
def main():
    """Yum repository management tool."""


@click.group('list')
def list_():
    """List subcommands."""


list_.add_command(list_all)
list_.add_command(list_nvrs)
list_.add_command(list_repos)

main.add_command(import_)
main.add_command(list_)
