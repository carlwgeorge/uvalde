import click

from uvalde.configuration import load_config


@click.command('list')
@click.option('-n', '--name', 'names', multiple=True, help='Limit output by package name.')
@click.option('-r', '--repo', 'repos', multiple=True, help='Limit output by repository.')
def list_(names, repos):
    """List RPM NVRs."""

    config = load_config()

    for repo in config:
        # repos filter
        if repos and str(repo) not in repos:
            continue

        click.secho(f'{repo}', fg='cyan')

        # look up NVRs based on SRPMS
        srcpkgdir = repo.base / 'src' / 'packages'
        for srpm in srcpkgdir.glob('**/*.rpm'):
            nvr = srpm.name.replace('.src.rpm', '')

            # names filter
            name, _, _ = nvr.rsplit('-', maxsplit=2)
            if names and name not in names:
                continue

            click.echo(f'  {nvr}')
