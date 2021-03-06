import configparser

import pytest


def write_config(path, parser):
    config_dir = path / '.config' / 'uvalde'
    config_dir.mkdir(parents=True)
    config_file = config_dir / 'repos.ini'
    with config_file.open('w') as f:
        parser.write(f)


@pytest.fixture
def tmp_config(tmp_path):
    parser = configparser.ConfigParser()
    for repo in ['repo1', 'repo2']:
        parser.add_section(repo)
        parser[repo]['base'] = str(tmp_path / repo)
        parser[repo]['architectures'] = 'i686, x86_64'
    write_config(tmp_path, parser)


@pytest.fixture
def tmp_config_missing_base(tmp_path):
    parser = configparser.ConfigParser()
    parser.add_section('repo1')
    parser['repo1']['architectures'] = 'i686, x86_64'
    write_config(tmp_path, parser)


@pytest.fixture
def tmp_config_missing_architectures(tmp_path):
    parser = configparser.ConfigParser()
    parser.add_section('repo1')
    parser['repo1']['base'] = str(tmp_path / 'repo1')
    write_config(tmp_path, parser)


@pytest.fixture
def tmp_config_mixed_architectures(tmp_path):
    parser = configparser.ConfigParser()
    for repo in ['repo1', 'repo2']:
        parser.add_section(repo)
        parser[repo]['base'] = str(tmp_path / repo)
    parser['repo1']['architectures'] = 'i686, x86_64'
    parser['repo2']['architectures'] = 'x86_64'
    write_config(tmp_path, parser)


@pytest.fixture
def tmp_config_architecture_not_configured(tmp_path):
    parser = configparser.ConfigParser()
    parser.add_section('repo1')
    parser['repo1']['base'] = str(tmp_path / 'repo1')
    parser['repo1']['architectures'] = 'i686'
    write_config(tmp_path, parser)


@pytest.fixture
def tmp_config_hidden(tmp_path):
    parser = configparser.ConfigParser()
    for repo in ['repo1', 'repo2']:
        parser.add_section(repo)
        parser[repo]['base'] = str(tmp_path / repo)
        parser[repo]['architectures'] = 'i686, x86_64'
    parser['repo1']['hidden'] = 'no'
    parser['repo2']['hidden'] = 'yes'
    write_config(tmp_path, parser)


@pytest.fixture(autouse=True)
def tmp_env(monkeypatch, tmp_path):
    # isolate config and database files to the testing directory
    monkeypatch.setenv('HOME', str(tmp_path))

    # force locale to keep click happy
    monkeypatch.setenv('LANG', 'C.UTF-8')


@pytest.fixture(autouse=True)
def mask_restorecon(monkeypatch):
    # segfaults in a container
    monkeypatch.setattr('selinux.restorecon', lambda x: None)
