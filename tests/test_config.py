import pathlib

import click.testing

import uvalde


def test_no_config(tmp_path):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list'])

    assert f'{tmp_path}/.config/uvalde/repos.ini: does not exist' in result.output
    assert result.exit_code == 1


def test_no_repo(tmp_config):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo0']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))

    result = runner.invoke(uvalde.main, args)

    assert f'repo0: repo not configured' in result.output
    assert result.exit_code == 1


def test_missing_base(tmp_config_missing_base):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list'])

    assert f'repo1: missing parameter base' in result.output
    assert result.exit_code == 1


def test_missing_architectures(tmp_config_missing_architectures):
    runner = click.testing.CliRunner()

    args = ['add', '--keep', '--repo', 'repo1']
    test_data = pathlib.Path('tests/data')
    args.extend(map(str, test_data.glob('*.rpm')))

    result = runner.invoke(uvalde.main, args)

    assert f'repo1: missing parameter architectures' in result.output
    assert result.exit_code == 1
