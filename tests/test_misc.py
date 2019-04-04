import click.testing

import uvalde


def test_no_config(tmp_path):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'repos'])

    assert f'{tmp_path}/.config/uvalde/repos.ini: does not exist' in result.output
    assert result.exit_code == 1


def test_no_repo(tmp_config):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'nvrs', 'repo0'])

    assert f'repo0: repo not configured' in result.output
    assert result.exit_code == 1
