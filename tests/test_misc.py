import click.testing

import uvalde


def test_no_config(tmp_path):
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'repos'])

    assert f'{tmp_path}/.config/uvalde/repos.ini: does not exist' in result.output
    assert result.exit_code == 1
