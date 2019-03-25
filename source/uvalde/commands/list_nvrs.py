import click
import createrepo_c

from uvalde.config import config


@click.command('nvrs')
@click.argument('repo')
def list_nvrs(repo):
    """List RPM NVRs in a repo."""

    config.load()
    srcpkgdir = config[repo].base / 'src' / 'packages'
    for srpm in srcpkgdir.glob('**/*.src.rpm'):
        pkg = createrepo_c.package_from_rpm(f'{srpm}')
        click.echo(f'{pkg.name}-{pkg.version}-{pkg.release}')
