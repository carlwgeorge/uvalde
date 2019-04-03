import click

from uvalde.import_ import import_
from uvalde.list_ import list_all, list_nvrs, list_repos
from uvalde.move import move


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
main.add_command(move)
