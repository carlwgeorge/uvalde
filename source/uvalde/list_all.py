import click
import createrepo_c

from uvalde.config import load_config


@click.command('all')
def list_all():
    """List configured repos and NVRs in each."""

    config = load_config()
    for repo in config:
        click.secho(f'{repo}', fg='cyan')
        srcpkgdir = repo.base / 'src' / 'packages'
        for path in srcpkgdir.glob('**/*.rpm'):
            pkg = createrepo_c.package_from_rpm(f'{path}')
            click.echo(f'  {pkg.name}-{pkg.version}-{pkg.release}')
