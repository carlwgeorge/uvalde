import shutil

import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR
from uvalde.repodata import createrepo
from uvalde.transfer import safe_check, remove_empty_parent


@click.command()
@click.option('--from', '-f', 'from_repo', prompt=True, help='Repository to move NVRs from.')
@click.option('--to', '-t', 'to_repo', prompt=True, help='Repository to move NVRs to.')
@click.argument('nvrs', nargs=-1)
def move(from_repo, to_repo, nvrs):
    """Move RPMs between repos."""

    config = load_config()
    from_base = config[from_repo].base
    to_base = config[to_repo].base
    if not config[from_repo].architectures == config[to_repo].architectures:
        raise SystemExit(f'configured architectures for {from_repo} and {to_repo} do not match')

    db = load_db()
    db.connect()

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
            start = from_base / artifact.path
            end = to_base / artifact.path
            safe_check(start, end)
            shutil.move(start, end)
            remove_empty_parent(start)

            # walk up the path to the directory createrepo needs to be run in
            # ex. /base/x86_64/ for /base/x86_64/packages/f/foo-1-1.rpm
            repodirs.add(start.parent.parent.parent)
            repodirs.add(end.parent.parent.parent)

    click.secho('generating repodata', fg='cyan')
    with click.progressbar(iterable=repodirs, fill_char='█') as repodirs_bar:
        for repodir in repodirs_bar:
            createrepo(repodir)
