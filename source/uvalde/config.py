import configparser
import pathlib

import appdirs
import click


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


class Config:
    """Object to access configured repos."""

    __slots__ = ['file', 'parser']

    def __init__(self):
        config_dir = pathlib.Path(appdirs.user_config_dir('uvalde'))
        if not config_dir.is_dir():
            config_dir.mkdir(parents=True)
        self.file = config_dir / 'repos.ini'
        self.parser = configparser.ConfigParser()

    def __iter__(self):
        for name in self.parser.sections():
            yield RepoConfig(self.parser[name])

    def __getitem__(self, repo):
        """Look up config section of repo."""

        try:
            return RepoConfig(self.parser[repo])
        except KeyError:
            raise SystemExit(click.style(f'{repo} repo not configured', fg='red'))

    def load(self):
        """Load repo configurations from config file."""

        if not self.file.exists():
            raise SystemExit(f'{self.file}: does not exist')
        self.parser.read(self.file)


config = Config()
