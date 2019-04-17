import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR
from uvalde.repodata import createrepo
from uvalde.transfer import remove_empty_parent


@click.command()
@click.option('--repo', '-r', prompt=True, help='Repository to remove NVRs from.')
@click.argument('nvrs', nargs=-1)
def remove(repo, nvrs):
    """Remove RPMs from repo."""

    config = load_config()
    base = config[repo].base

    db = load_db()
    db.connect()

    repodirs = set()
    artifacts = []

    with db.atomic():
        for label in nvrs:
            nvr = NVR.get(label=label)
            artifacts.extend(nvr.artifacts)
    db.close()

    click.secho('deleting RPMs', fg='cyan')
    with click.progressbar(iterable=artifacts, fill_char='█') as artifacts_bar:
        for artifact in artifacts_bar:
            target = base / artifact.path
            target.unlink()
            remove_empty_parent(target)

            # walk up the path to the directory createrepo needs to be run in
            # ex. /base/x86_64/ for /base/x86_64/packages/f/foo-1-1.rpm
            repodirs.add(target.parent.parent.parent)

    click.secho('generating repodata', fg='cyan')
    with click.progressbar(iterable=repodirs, fill_char='█') as repodirs_bar:
        for repodir in repodirs_bar:
            createrepo(repodir)
