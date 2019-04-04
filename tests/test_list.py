import click.testing

import uvalde


def test_list_repos():
    runner = click.testing.CliRunner()

    result = runner.invoke(uvalde.main, ['list', 'repos'])

    assert result.exit_code == 0
    assert 'repo1' in result.output
    assert 'repo2' in result.output
