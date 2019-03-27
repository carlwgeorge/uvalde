import configparser
import pathlib

import appdirs
import click


def load_config():
    """Load configurations from config file."""

    config_dir = pathlib.Path(appdirs.user_config_dir('uvalde'))
    if not config_dir.is_dir():
        config_dir.mkdir(parents=True)
    config_file = config_dir / 'repos.ini'
    if not config_file.exists():
        raise SystemExit(f'{config_file}: does not exist')
    return Config(config_file)


class Config:
    """Object to access configured repos."""

    __slots__ = ['parser']

    def __init__(self, config_file):
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)

    def __iter__(self):
        for name in self.parser.sections():
            yield RepoConfig(self.parser[name])

    def __getitem__(self, repo):
        try:
            return RepoConfig(self.parser[repo])
        except KeyError:
            raise SystemExit(click.style(f'{repo} repo not configured', fg='red'))


class RepoConfig:
    """Object to access settings for a repo."""

    __slots__ = ['section']

    def __init__(self, section):
        self.section = section

    def __str__(self):
        return self.section.name

    @property
    def base(self):
        """Look up base setting of repo."""

        try:
            return pathlib.Path(self.section['base'])
        except KeyError:
            raise SystemExit(click.style('missing parameter base', fg='red'))

    @property
    def architectures(self):
        """Look up architectures setting of repo."""

        try:
            return [
                architecture.strip()
                for architecture in self.section['architectures'].split(',')
            ]
        except KeyError:
            raise SystemExit(click.style('missing parameter architectures', fg='red'))
