import click
import createrepo_c

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR, Artifact


@click.command()
@click.argument('repos', nargs=-1)
def index(repos):
    """Index existing repo tree."""

    config = load_config()
    db = load_db()

    with db.atomic():
        db.create_tables([NVR, Artifact])

        for repo in repos:
            base = config[repo].base
            architectures = config[repo].architectures
            click.secho(f'indexing repo {repo}', fg='cyan')

            rpms = list(base.glob('**/*.rpm'))
            with click.progressbar(iterable=rpms, fill_char='█') as rpms_bar:
                for rpm in rpms_bar:
                    # read metadata from RPM file
                    pkg = createrepo_c.package_from_rpm(f'{rpm}')

                    # record NVR label in database
                    if pkg.arch == 'src':
                        label = f'{pkg.name}-{pkg.version}-{pkg.release}'
                    else:
                        label = pkg.rpm_sourcerpm[:-8]
                    nvr, _ = NVR.get_or_create(label=label)

                    if pkg.arch == 'noarch':
                        # noarch path could be in any architectures
                        possible_destinations = [
                            base / architecture / 'packages' / rpm.name[0] / rpm.name
                            for architecture in architectures
                        ]

                        if rpm not in possible_destinations:
                            raise SystemExit(f'{rpm.name}: not in expected location')

                    else:
                        # ensure the incoming architecture matches one of the configured architectures
                        if pkg.arch != 'src' and pkg.arch not in architectures:
                            raise SystemExit(f'{rpm.name}: architecture not configured for repo {repo}')

                        # compute destination path
                        if pkg.name.endswith('-debuginfo') or pkg.name.endswith('-debugsource'):
                            destination = base / pkg.arch / 'debug' / 'packages' / rpm.name[0] / rpm.name
                        else:
                            destination = base / pkg.arch / 'packages' / rpm.name[0] / rpm.name

                        if destination != rpm:
                            raise SystemExit(f'{rpm.name}: not in expected location')

                    artifact, _ = Artifact.get_or_create(nvr=nvr, path=rpm.relative_to(base))

    db.close()
