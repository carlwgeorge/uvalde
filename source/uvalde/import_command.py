import pathlib

import click
import createrepo_c

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR, Artifact
from uvalde.repodata import createrepo
from uvalde.transfer import safe_copy, safe_move


@click.command('import')
@click.option('--keep-original', '-k', is_flag=True)
@click.argument('repo')
@click.argument('rpms', type=pathlib.Path, nargs=-1)
def import_(keep_original, repo, rpms):
    """Import RPM files to a repo."""

    config = load_config()
    base = config[repo].base
    architectures = config[repo].architectures

    db = load_db()
    db.connect()

    repodirs = set()

    with db.atomic():
        db.create_tables([NVR, Artifact])
        for rpm in rpms:
            # read metadata from RPM file
            pkg = createrepo_c.package_from_rpm(f'{rpm}')

            if pkg.arch == 'noarch':
                # record NVR in database
                label = pkg.rpm_sourcerpm.rstrip('.src.rpm')
                nvr, _ = NVR.get_or_create(label=label)

                # noarch goes in all architectures
                for architecture in architectures:
                    # compute destination path
                    repodirs.add(base / architecture)
                    destination = base / architecture / 'packages' / rpm.name[0] / rpm.name

                    # record Artifact in database
                    artifact, _ = Artifact.get_or_create(nvr=nvr, path=destination.relative_to(base))

                    # move RPM file to destination
                    safe_copy(rpm, destination)

                if not keep_original:
                    rpm.unlink()
            else:
                # ensure the incoming architecture matches one of the configured architectures
                if pkg.arch != 'src' and pkg.arch not in architectures:
                    raise SystemExit(f'{rpm.name}: architecture not configured for {repo}')

                # record NVR in database
                if pkg.rpm_sourcerpm:
                    label = pkg.rpm_sourcerpm.rstrip('.src.rpm')
                else:
                    # if pkg doesn't have the rpm_sourcerpm attribute, it's a SRPM itself
                    label = f'{pkg.name}-{pkg.version}-{pkg.release}'
                nvr, _ = NVR.get_or_create(label=label)

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
                if keep_original:
                    safe_copy(rpm, destination)
                else:
                    safe_move(rpm, destination)

    db.close()

    for repodir in repodirs:
        createrepo(repodir)
