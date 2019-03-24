import configparser
import pathlib

import appdirs


class Config:
    """Object to access configured repos."""

    __slots__ = ['file', 'parser']

    def __init__(self):
        config_dir = pathlib.Path(appdirs.user_config_dir('uvalde'))
        if not config_dir.is_dir():
            config_dir.mkdir(parents=True)
        self.file = config_dir / 'repos.ini'
        self.parser = configparser.ConfigParser()

    def load(self):
        """Load repo configurations from config file."""

        if not self.file.exists():
            raise SystemExit(f'{self.file}: does not exist')
        self.parser.read(self.file)


config = Config()
