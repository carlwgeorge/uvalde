import click

from uvalde.config import config
from uvalde.database import db, NVR
from uvalde.transfer import safe_move


@click.command()
@click.argument('from-repo')
@click.argument('to-repo')
@click.argument('nvrs', nargs=-1)
def move(from_repo, to_repo, nvrs):
    """Move RPMs between repos."""

    config.load()
    from_base = config[from_repo].base
    to_base = config[to_repo].base
    if not config[from_repo].architectures == config[to_repo].architectures:
        raise SystemExit(click.style(f'configured architectures for {from_repo} and {to_repo} do not match', fg='red'))

    db.connect()

    for label in nvrs:
        nvr = NVR.get(label=label)
        for artifact in nvr.artifacts:
            start = from_base / artifact.path
            end = to_base / artifact.path
            safe_move(start, end, cleanup=True)

    db.close()
