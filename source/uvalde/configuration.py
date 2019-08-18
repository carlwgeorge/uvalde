import configparser
import pathlib

import appdirs


def load_config():
    """Load configurations from config file."""

    config_dir = pathlib.Path(appdirs.user_config_dir('uvalde'))
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
            raise SystemExit(f'{repo}: repo not configured')


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
            raise SystemExit(f'{self}: missing parameter base')

    @property
    def architectures(self):
        """Look up architectures setting of repo."""

        try:
            return [
                architecture.strip()
                for architecture in self.section['architectures'].split(',')
            ]
        except KeyError:
            raise SystemExit(f'{self}: missing parameter architectures')

    @property
    def hidden(self):
        """Look up hidden setting of repo."""

        try:
            raw = self.section['hidden']
            if raw in ['1', 'y', 'Y', 'yes', 'Yes', 'YES', 'true', 'True', 'TRUE', 'on', 'On', 'ON']:
                return True
            elif raw in ['0', 'n', 'N', 'no', 'No', 'NO', 'false', 'False', 'FALSE', 'off', 'Off', 'OFF']:
                return False
        except KeyError:
            pass

        return False
