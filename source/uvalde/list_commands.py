import click

from uvalde.configuration import load_config


@click.command('all')
def list_all():
    """List configured repos and NVRs in each."""

    config = load_config()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
        srcpkgdir = repo.base / 'src' / 'packages'
        for srpm in srcpkgdir.glob('**/*.rpm'):
            nvr = srpm.name.replace('.src.rpm', '')
            click.echo(f'  {nvr}')


@click.command('nvrs')
@click.argument('repo')
def list_nvrs(repo):
    """List RPM NVRs in a repo."""

    config = load_config()
    srcpkgdir = config[repo].base / 'src' / 'packages'
    for srpm in srcpkgdir.glob('**/*.src.rpm'):
        nvr = srpm.name.replace('.src.rpm', '')
        click.echo(f'{nvr}')


@click.command('repos')
def list_repos():
    """List configured repos."""

    config = load_config()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
