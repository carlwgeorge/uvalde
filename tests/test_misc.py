import click.testing

import uvalde


def test_no_config(tmp_path):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['config', 'show', 'repo0'])

    assert f'{tmp_path}/.config/uvalde/repos.ini: does not exist' in result.output
    assert result.exit_code == 1


def test_no_repo(tmp_config):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['config', 'show', 'repo0'])

    assert f'repo0: repo not configured' in result.output
    assert result.exit_code == 1


def test_missing_base(tmp_config_missing_base):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['config', 'show', 'repo1'])

    assert f'repo1: missing parameter base' in result.output
    assert result.exit_code == 1


def test_missing_architectures(tmp_config_missing_architectures):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['config', 'show', 'repo1'])

    assert f'repo1: missing parameter architectures' in result.output
    assert result.exit_code == 1
