import configparser

import pytest


@pytest.fixture(autouse=True)
def tmp_config(tmp_path):
    parser = configparser.ConfigParser()
    for repo in ['repo1', 'repo2']:
        parser.add_section(repo)
        parser[repo]['base'] = str(tmp_path / repo)
        parser[repo]['architectures'] = 'i686, x86_64'

    config_dir = tmp_path / '.config' / 'uvalde'
    config_dir.mkdir(parents=True)
    config_file = config_dir / 'repos.ini'
    with config_file.open('w') as f:
        parser.write(f)
