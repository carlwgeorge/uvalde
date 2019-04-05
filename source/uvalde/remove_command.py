import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR
from uvalde.repodata import createrepo


@click.command()
@click.argument('repo')
@click.argument('nvrs', nargs=-1)
def remove(repo, nvrs):
    """Remove RPMs from repo."""

    config = load_config()
    base = config[repo].base

    db = load_db()
    db.connect()

    repodirs = set()

    for label in nvrs:
        nvr = NVR.get(label=label)
        for artifact in nvr.artifacts:
            target = base / artifact.path
            output = click.style(f'{target}', fg='cyan')
            x = click.style('X', fg='red')
            click.echo(f'{output} {x}')
            target.unlink()

            # walk up the path to the directory createrepo needs to be run in
            # ex. /base/x86_64/ for /base/x86_64/packages/f/foo-1-1.rpm
            repodirs.add(target.parent.parent.parent)

    db.close()

    for repodir in repodirs:
        createrepo(repodir)
