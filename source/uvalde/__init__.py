import click

from uvalde.commands.list_repos import list_repos


@click.group()
def main():
    """Yum repository management tool."""


@click.group('list')
def list_():
    """List subcommands."""


list_.add_command(list_repos)

main.add_command(list_)
