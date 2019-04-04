import click

from uvalde.configuration import load_config


@click.command('show')
@click.argument('repo')
def config_show(repo):
    """Show configuration settings for a repo."""

    config = load_config()

    click.secho(f'[{config[repo]}]', fg='green')

    key = click.style('base', fg='yellow')
    value = click.style(str(config[repo].base), fg='green')
    click.echo(f'{key} = {value}')

    key = click.style('architectures', fg='yellow')
    value = click.style(', '.join(config[repo].architectures), fg='green')
    click.echo(f'{key} = {value}')
