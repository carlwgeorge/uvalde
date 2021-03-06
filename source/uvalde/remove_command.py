import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR
from uvalde.repodata import createrepo
from uvalde.transfer import remove_empty_parent


@click.command()
@click.option('-r', '--repo', prompt=True, help='Repository to remove NVRs from.')
@click.argument('nvrs', required=True, nargs=-1)
def remove(repo, nvrs):
    """Remove RPMs from repo."""

    config = load_config()
    db = load_db()

    base = config[repo].base
    architectures = config[repo].architectures
    prefix = config[repo].prefix

    click.secho('removing RPMs', fg='cyan')

    # remember repo directories we've touched so we can regenerate repodata
    repodirs = set()
    artifacts = []

    for label in nvrs:
        # ensure nvr is in repo
        srcpkgdir = base / 'src'
        for srpm in srcpkgdir.glob('**/*.rpm'):
            if srpm.name == f'{label}.src.rpm':
                break
        else:
            raise SystemExit(f'{label} not found in repo {repo}')

        # collect artifacts
        nvr = NVR.get(label=label)
        artifacts.extend(nvr.artifacts)

    with click.progressbar(iterable=artifacts, fill_char='█') as artifacts_bar:
        for artifact in artifacts_bar:
            if artifact.architecture == 'noarch':
                # noarch is in all architectures
                for architecture in architectures:
                    repodirs.add(base / architecture)
                    path = (
                        base / architecture /
                        prefix.format(artifact.filename) / artifact.filename
                    )

                    # remove file
                    path.unlink()
                    remove_empty_parent(path)

            else:
                if artifact.debug:
                    repodirs.add(base / artifact.architecture / 'debug')
                    path = (
                        base / artifact.architecture / 'debug' /
                        prefix.format(artifact.filename) / artifact.filename
                    )

                else:
                    repodirs.add(base / artifact.architecture)
                    path = (
                        base / artifact.architecture /
                        prefix.format(artifact.filename) / artifact.filename
                    )

                # remove file
                path.unlink()
                remove_empty_parent(path)

    db.close()

    click.secho('generating repodata', fg='cyan')
    with click.progressbar(iterable=repodirs, fill_char='█') as repodirs_bar:
        for repodir in repodirs_bar:
            createrepo(repodir)
