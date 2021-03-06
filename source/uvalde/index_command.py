import click
import createrepo_c

from uvalde.configuration import load_config
from uvalde.database import load_db, NVR, Artifact


@click.command()
@click.argument('repos', required=True, nargs=-1)
def index(repos):
    """Index existing repo tree."""

    config = load_config()
    db = load_db()

    with db.atomic():
        for repo in repos:
            base = config[repo].base
            architectures = config[repo].architectures
            prefix = config[repo].prefix
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
                            base / architecture / prefix.format(rpm.name) / rpm.name
                            for architecture in architectures
                        ]

                        if rpm not in possible_destinations:
                            raise SystemExit(f'{rpm.name}: not in expected location')

                        # record artifact in database
                        artifact, _ = Artifact.get_or_create(
                            nvr=nvr,
                            filename=rpm.name,
                            architecture=pkg.arch,
                        )

                    else:
                        # ensure the incoming architecture matches one of the configured architectures
                        if pkg.arch != 'src' and pkg.arch not in architectures:
                            raise SystemExit(f'{rpm.name}: architecture not configured for repo {repo}')

                        # remember if it's a debuginfo or debugsource package
                        debug = pkg.name.endswith('-debuginfo') or pkg.name.endswith('-debugsource')

                        # compute destination path
                        if debug:
                            destination = base / pkg.arch / 'debug' / prefix.format(rpm.name) / rpm.name
                        else:
                            destination = base / pkg.arch / prefix.format(rpm.name) / rpm.name

                        if destination != rpm:
                            raise SystemExit(f'{rpm.name}: not in expected location')

                        # record artifact in database
                        artifact, _ = Artifact.get_or_create(
                            nvr=nvr,
                            filename=rpm.name,
                            architecture=pkg.arch,
                            debug=debug,
                        )

    db.close()
