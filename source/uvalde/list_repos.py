import click

from uvalde.config import load_config


@click.command('repos')
def list_repos():
    """List configured repos."""

    config = load_config()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
