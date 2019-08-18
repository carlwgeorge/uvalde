import shutil

import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR
from uvalde.repodata import createrepo
from uvalde.transfer import safe_check, remove_empty_parent


@click.command()
@click.option('-f', '--from', 'from_repo', prompt=True, help='Repository to move NVRs from.')
@click.option('-t', '--to', 'to_repo', prompt=True, help='Repository to move NVRs to.')
@click.argument('nvrs', nargs=-1)
def move(from_repo, to_repo, nvrs):
    """Move RPMs between repos."""

    config = load_config()
    db = load_db()

    from_base = config[from_repo].base
    to_base = config[to_repo].base

    from_prefix = config[from_repo].prefix
    to_prefix = config[to_repo].prefix

    from_architectures = config[from_repo].architectures
    to_architectures = config[to_repo].architectures
    if not from_architectures == to_architectures:
        raise SystemExit(f'configured architectures for {from_repo} and {to_repo} do not match')
    architectures = from_architectures

    repodirs = set()
    artifacts = []

    with db.atomic():
        for label in nvrs:
            nvr = NVR.get(label=label)
            artifacts.extend(nvr.artifacts)
    db.close()

    click.secho('moving RPMs', fg='cyan')
    with click.progressbar(iterable=artifacts, fill_char='█') as artifacts_bar:
        for artifact in artifacts_bar:
            if artifact.architecture == 'noarch':
                # noarch goes in all architectures
                for architecture in architectures:
                    repodirs.add(from_base / architecture)
                    repodirs.add(to_base / architecture)

                    from_path = (
                        from_base / architecture /
                        from_prefix.format(artifact.filename) / artifact.filename
                    )
                    to_path = (
                        to_base / architecture /
                        to_prefix.format(artifact.filename) / artifact.filename
                    )

                    safe_check(from_path, to_path)
                    shutil.move(from_path, to_path)
                    remove_empty_parent(from_path)

            else:
                if artifact.debug:
                    repodirs.add(from_base / artifact.architecture / 'debug')
                    repodirs.add(to_base / artifact.architecture / 'debug')

                    from_path = (
                        from_base / artifact.architecture / 'debug' /
                        from_prefix.format(artifact.filename) / artifact.filename
                    )
                    to_path = (
                        to_base / artifact.architecture / 'debug' /
                        to_prefix.format(artifact.filename) / artifact.filename
                    )

                else:
                    repodirs.add(from_base / artifact.architecture)
                    repodirs.add(to_base / artifact.architecture)

                    from_path = (
                        from_base / artifact.architecture /
                        from_prefix.format(artifact.filename) / artifact.filename
                    )
                    to_path = (
                        to_base / artifact.architecture /
                        to_prefix.format(artifact.filename) / artifact.filename
                    )

                safe_check(from_path, to_path)
                shutil.move(from_path, to_path)
                remove_empty_parent(from_path)

    click.secho('generating repodata', fg='cyan')
    with click.progressbar(iterable=repodirs, fill_char='█') as repodirs_bar:
        for repodir in repodirs_bar:
            createrepo(repodir)
