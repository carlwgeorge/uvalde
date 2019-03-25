import click

from uvalde.config import config


@click.command('repos')
def list_repos():
    """List configured repos."""

    config.load()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
