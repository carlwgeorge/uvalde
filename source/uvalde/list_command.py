import click
import createrepo_c

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

        labels = set()

        # scan filesystem for RPMS
        for rpm in repo.base.glob('**/*.rpm'):
            # read metadata from RPM file
            pkg = createrepo_c.package_from_rpm(f'{rpm}')
            if pkg.arch == 'src':
                label = f'{pkg.name}-{pkg.version}-{pkg.release}'
            else:
                label = pkg.rpm_sourcerpm[:-8]

            # ensure NVR is in database
            if not NVR.get_or_none(label=label):
                raise SystemExit(
                    f'{rpm.name} found in repo directory but {label} is not in the database.  '
                    'Run `uvalde index` to correct this.'
                )

            # names filter
            name, _, _ = label.rsplit('-', maxsplit=2)
            if names and name not in names:
                continue

            labels.add(label)

        for label in labels:
            click.echo(f'  {label}')

    db.close()
