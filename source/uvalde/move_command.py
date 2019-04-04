import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR
from uvalde.repodata import createrepo
from uvalde.transfer import safe_move


@click.command()
@click.argument('from-repo')
@click.argument('to-repo')
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

    for label in nvrs:
        nvr = NVR.get(label=label)
        for artifact in nvr.artifacts:
            start = from_base / artifact.path
            end = to_base / artifact.path
            safe_move(start, end, cleanup=True)

            # walk up the path to the directory createrepo needs to be run in
            # ex. /base/x86_64/ for /base/x86_64/packages/f/foo-1-1.rpm
            repodirs.add(start.parent.parent.parent)
            repodirs.add(end.parent.parent.parent)

    db.close()

    for repodir in repodirs:
        createrepo(repodir)
