import click

from uvalde.import_command import import_
from uvalde.list_command import list_
from uvalde.move_command import move
from uvalde.remove_command import remove


@click.group()
def main():
    """Yum repository management tool."""


main.add_command(import_)
main.add_command(list_)
main.add_command(move)
main.add_command(remove)
