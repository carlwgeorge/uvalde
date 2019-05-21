import pathlib
import shutil

import click
import createrepo_c
import selinux

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR, Artifact
from uvalde.repodata import createrepo
from uvalde.transfer import safe_check


@click.command('import')
@click.option('-k', '--keep', is_flag=True, help='Keep original RPM files.')
@click.option('-r', '--repo', prompt=True, help='Repository to import RPMs into.')
@click.argument('rpms', type=pathlib.Path, nargs=-1)
def import_(keep, repo, rpms):
    """Import RPM files to a repo."""

    config = load_config()
    base = config[repo].base
    architectures = config[repo].architectures

    db = load_db()
    db.connect()

    repodirs = set()

    click.secho('importing RPMs', fg='cyan')
    with db.atomic():
        db.create_tables([NVR, Artifact])
        with click.progressbar(iterable=rpms, fill_char='█') as rpms_bar:
            for rpm in rpms_bar:
                # read metadata from RPM file
                pkg = createrepo_c.package_from_rpm(f'{rpm}')

                # record NVR label in database
                if pkg.arch == 'src':
                    label = f'{pkg.name}-{pkg.version}-{pkg.release}'
                else:
                    label = pkg.rpm_sourcerpm[:-8]
                nvr, _ = NVR.get_or_create(label=label)

                if pkg.arch == 'noarch':
                    # noarch goes in all architectures
                    for architecture in architectures:
                        # compute destination path
                        repodirs.add(base / architecture)
                        destination = base / architecture / 'packages' / rpm.name[0] / rpm.name

                        # record Artifact in database
                        artifact, _ = Artifact.get_or_create(nvr=nvr, path=destination.relative_to(base))

                        # move RPM file to destination
                        safe_check(rpm, destination)
                        shutil.copy2(rpm, destination)
                        selinux.restorecon(destination)

                    if not keep:
                        rpm.unlink()
                else:
                    # ensure the incoming architecture matches one of the configured architectures
                    if pkg.arch != 'src' and pkg.arch not in architectures:
                        raise SystemExit(f'{rpm.name}: architecture not configured for {repo}')

                    # compute destination path
                    if pkg.name.endswith('-debuginfo') or pkg.name.endswith('-debugsource'):
                        repodirs.add(base / pkg.arch / 'debug')
                        destination = base / pkg.arch / 'debug' / 'packages' / rpm.name[0] / rpm.name
                    else:
                        repodirs.add(base / pkg.arch)
                        destination = base / pkg.arch / 'packages' / rpm.name[0] / rpm.name

                    # record Artifact in database
                    artifact, _ = Artifact.get_or_create(nvr=nvr, path=destination.relative_to(base))

                    # move RPM file to destination
                    if keep:
                        safe_check(rpm, destination)
                        shutil.copy2(rpm, destination)
                    else:
                        safe_check(rpm, destination)
                        shutil.move(rpm, destination)
                    selinux.restorecon(destination)

    db.close()

    click.secho('generating repodata', fg='cyan')
    with click.progressbar(iterable=repodirs, fill_char='█') as repodirs_bar:
        for repodir in repodirs_bar:
            createrepo(repodir)
