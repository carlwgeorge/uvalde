import pathlib

import click

from uvalde.config import config
from uvalde.transfer import safe_copy, safe_move


@click.command('import')
@click.argument('repo')
@click.argument('rpms', type=pathlib.Path, nargs=-1)
def import_(repo, rpms):
    """Import RPM files to a repo."""

    config.load()
    base = config[repo].base
    architectures = config[repo].architectures

    for rpm in rpms:
        # read metadata from RPM file
        pkg = createrepo_c.package_from_rpm(f'{rpm}')

        # move RPM file to destination
        if pkg.arch == 'noarch':
            # noarch goes in all architectures
            for architecture in architectures:
                destination = base / architecture / 'packages' / rpm.name[0] / rpm.name
                safe_copy(rpm, destination)
            rpm.unlink()
        else:
            if pkg.name.endswith('-debuginfo') or pkg.name.endswith('-debugsource'):
                destination = base / pkg.arch / 'debug' / 'packages' / rpm.name[0] / rpm.name
            else:
                destination = base / pkg.arch / 'packages' / rpm.name[0] / rpm.name
            safe_move(rpm, destination)

