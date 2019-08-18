import click

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR


@click.command('list')
@click.option('-n', '--name', 'names', multiple=True, help='Limit output by package name.')
@click.option('-r', '--repo', 'repos', multiple=True, help='Limit output by repository.')
@click.option('-a', '--all', 'all_', is_flag=True, help='Include hidden repositories.')
def list_(names, repos, all_):
    """List RPM NVRs."""

    config = load_config()
    db = load_db()

    for repo in config:
        # filter repos
        if repos and str(repo) not in repos:
            continue
        if not all_ and not repos and repo.hidden:
            continue

        click.secho(f'{repo}', fg='cyan')

        # look up NVRs based on SRPMS
        srcpkgdir = repo.base / 'src'
        for srpm in srcpkgdir.glob('**/*.rpm'):
            nvr = srpm.name.replace('.src.rpm', '')

            # ensure NVR is in database
            if not NVR.get_or_none(label=nvr):
                raise SystemExit(
                    f'{nvr} found in repo directory but not in database.  '
                    'Run `uvalde index` to correct this.'
                )

            # names filter
            name, _, _ = nvr.rsplit('-', maxsplit=2)
            if names and name not in names:
                continue

            click.echo(f'  {nvr}')

    db.close()
