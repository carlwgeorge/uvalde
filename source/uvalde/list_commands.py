import click

from uvalde.configuration import load_config


@click.command('all')
@click.option('-n', '--name', 'names', multiple=True, help='Limit output by package name.')
def list_all(names):
    """List configured repos and NVRs in each."""

    config = load_config()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
        srcpkgdir = repo.base / 'src' / 'packages'
        for srpm in srcpkgdir.glob('**/*.rpm'):
            nvr = srpm.name.replace('.src.rpm', '')
            name, _, _ = nvr.rsplit('-', maxsplit=2)
            if not names or name in names:
                click.echo(f'  {nvr}')


@click.command('nvrs')
@click.option('-n', '--name', 'names', multiple=True, help='Limit output by package name.')
@click.argument('repo')
def list_nvrs(names, repo):
    """List RPM NVRs in a repo."""

    config = load_config()
    srcpkgdir = config[repo].base / 'src' / 'packages'
    for srpm in srcpkgdir.glob('**/*.src.rpm'):
        nvr = srpm.name.replace('.src.rpm', '')
        name, _, _ = nvr.rsplit('-', maxsplit=2)
        if not names or name in names:
            click.echo(f'{nvr}')


@click.command('repos')
def list_repos():
    """List configured repos."""

    config = load_config()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
